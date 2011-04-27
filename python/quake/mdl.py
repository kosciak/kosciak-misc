#!/usr/bin/env python

"""mdl.py - classes representing Quake 1 MDL files, and loader."""

import math
import os.path
import struct
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


__author__ = "Wojciech 'KosciaK' Pietrzok"


class TextureCoord(object):

    """Texture coordinates.

    s - x coordinate, t - y coordinate, onseam - both front and back

    """

    def __init__(self, onseam, s, t):
        self.onseam = onseam
        self.s = s
        self.t = t

    def __str__(self):
        return '<TextureCoord onseam=%s, s=%s, t=%s>' %  \
                (self.onseam, self.s, self.t)


class Triangle(object):

    """Contains Vertices indexes."""

    def __init__(self, facesfront, *vertindex):
        self.facesfront = facesfront
        if len(vertindex) != 3:
            raise ValueError('Invalid number of vertices!')
        self.vertindex = vertindex

    def __str__(self):
        return '<Triangle facesfront=%s, vertindex=%s>' % \
                (self.facesfront, self.vertindex)


class Vector(object):

    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '<Vector [%.5f, %.5f, %.5f]>' % (self.x, self.y, self.z)


class Vertex(Vector):

    """Scaled and translated vector,

    with information if it belongs to front, or back of the model.
    normal_index - index of normal vector (see anorms.py)
    
    """

    NONE_SCALE = Vector(1, 1, 1)
    NONE_TRANSLATE = Vector(0, 0, 0)

    def __init__(self, x, y, z, normal_index,
                 scale=NONE_SCALE, translate=NONE_TRANSLATE):
        Vector.__init__(self, 
                        x * scale.x + translate.x, 
                        y * scale.y + translate.y, 
                        z * scale.z + translate.z)
        self.raw = (x, y, z)
        self.normal_index = normal_index

    def __str__(self):
        return '<Vertex [%.5f, %.5f, %.5f] normal=%s>' % \
                (self.x, self.y, self.z, self.normal_index)


class SimpleFrame(object):

    """List of Vertices coordinates for current frame."""

    type = 0

    def __init__(self, bboxmin, bboxmax, name, verts):
        self.bboxmin = bboxmin
        self.bboxmax = bboxmax
        self.name = name
        self.verts = verts


class Skin(object):

    """Raws skin data.

    List of color indexes (see colormap.py for RGB values).

    """

    group = 0

    def __init__(self, data):
        self.data = data


class Header(object):

    """Header of the MDL file."""

    ident = 1330660425 # little-endian IDPO
    version = 6

    def __init__(self, scale, translate,
                 boundingradius, eyeposition,
                 num_skins, skinwidth, skinheight,
                 num_verts, num_tris, num_frames,
                 synctype, flags, size):
        self.scale = scale
        self.translate = translate
        self.boundingradius = boundingradius
        self.eyeposition = eyeposition
        self.num_skins = num_skins
        self.skinwidth = skinwidth
        self.skinheight = skinheight
        self.num_verts = num_verts
        self.num_tris = num_tris
        self.num_frames = num_frames
        self.synctype = synctype
        self.flags = flags
        self.size = size


class Model(object):

    """Quake 1 MDL file."""

    def __init__(self, name):
        self.name = name
        self.header = None
        self.skins = []
        self.texcoords = []
        self.triangles = []
        self.frames = []

    @property
    def skinwidth(self):
        return self.header.skinwidth

    @property
    def skinheight(self):
        return self.header.skinheight


class Loader(object):

    """Loader of Quake 1 MDL files.
    
    Skin groups, and frame groups are not supported.

    See http://tfc.duke.free.fr/coding/mdl-specs-en.html
    for file structure reference.
    
    """

    header_struct = struct.Struct('<ii3f3ff3fiiiiiiiif')
    texturecoord_struct = struct.Struct('<iii')
    triangle_struct = struct.Struct('<i3i')
    vertex_struct = struct.Struct('<3BB')

    def __init__(self, path):
        if not os.path.isfile(path):
            raise ValueError('Not a file: %s' % path)
        self.path = path

    def load(self):
        name = os.path.basename(self.path)
        if '.' in name:
            name = name[:name.find('.')]
        mdl = Model(name)
        file = open(self.path, 'rb')
        header = self.load_header(file)
        mdl.header = header
        for i in range(header.num_skins):
            skin = self.load_skin(file, header)
            mdl.skins.append(skin)
        for i in range(header.num_verts):
            texcoord = self.load_texturecoords(file)
            mdl.texcoords.append(texcoord)
        for i in range(header.num_tris):
            triangle = self.load_triangle(file)
            mdl.triangles.append(triangle)
        for i in range(header.num_frames):
            frame = self.load_frame(file, header)
            mdl.frames.append(frame)
        file.close()
        return mdl

    def load_header(self, file):
        struct_size = self.header_struct.size
        bytes = file.read(struct_size)
        data = self.header_struct.unpack(bytes)
        if data[0] != Header.ident or \
           data[1] != Header.version:
            raise ValueError('Invalid ident or version')
        scale = Vector(*data[2:5])
        translate = Vector(*data[5:8])
        eyeposition = Vector(*data[9:12])
        return Header(scale, translate,
                      data[8], eyeposition,
                      *data[12:])

    def load_skin(self, file, header):
        group = struct.unpack('<i', file.read(4))[0]
        if group:
            raise ValueError('Skin groups not supported!')
        skin_size = header.skinwidth * header.skinheight
        data = struct.unpack('<%sb' % skin_size, file.read(skin_size))
        return Skin(data)

    def load_texturecoords(self, file):
        struct_size = self.texturecoord_struct.size
        bytes = file.read(struct_size)
        data = self.texturecoord_struct.unpack(bytes)
        return TextureCoord(*data)

    def load_triangle(self, file):
        struct_size = self.triangle_struct.size
        bytes = file.read(struct_size)
        data = self.triangle_struct.unpack(bytes)
        return Triangle(*data)

    def load_frame(self, file, header):
        vert_struct_size = self.vertex_struct.size
        type = struct.unpack('<i', file.read(4))[0]
        if type:
            # flame.mdl, flame2.mdl contain group frames
            raise ValueError('Frame groups not supported!')
        struct_size = 2 * vert_struct_size + 16 + \
                      header.num_verts * vert_struct_size
        file = StringIO(file.read(struct_size))
        bboxmin = self.load_vertex(file, header.scale, header.translate)
        bboxmax = self.load_vertex(file, header.scale, header.translate)
        raw_name = struct.unpack('<16s', file.read(16))[0]
        name = raw_name[:raw_name.find('\x00')]
        verts = []
        for i in range(header.num_verts):
            vert = self.load_vertex(file, header.scale, header.translate)
            verts.append(vert)
        file.close()
        return SimpleFrame(bboxmin, bboxmax, name, verts)

    def load_vertex(self, file, scale, translate):
        struct_size = self.vertex_struct.size
        bytes = file.read(struct_size)
        data = self.vertex_struct.unpack(bytes)
        return Vertex(data[0], data[1], data[2], data[3], scale, translate)


# TODO: Writer ?


def load(path):
    loader = Loader(path)
    return loader.load()


if __name__ == '__main__':
    mdl_file = sys.argv[1]
    model = load(mdl_file)

    print 'Model: %s' % model.name
    print 'Scale: %s' % model.header.scale
    print 'Tranlslate: %s' % model.header.translate
    print 'Skin (%s x %s) - TextureCoords:' % (model.skinwidth, 
                                               model.skinheight)
    for i, texcoord in enumerate(model.texcoords):
        print '%s: %s' % (i, texcoord)
    print 'Triangles:'
    for i, triangle in enumerate(model.triangles):
        print '%s: %s' % (i, triangle)
    print 'Frame %s/%s: %s' % (0, model.header.num_frames, model.frames[0].name)
    for i, vertex in enumerate(model.frames[0].verts):
        print '%s: %s' % (i, vertex)

