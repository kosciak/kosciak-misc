#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cairo, pango, pangocairo


to_render = [
    ('pl', 'zażółć gęślą jaźń'),
    ('ar', 'مَقْلُوب رَاسًا على عَقْبٍ'),
]

WIDTH = 375
HEIGHT = 50

FOREGROUND = (0, 0, 0)
BACKGROUND = (255, 255, 255)


font_description = pango.FontDescription('DejaVuSans 24')

for filename, text in to_render:
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    cairo_context = cairo.Context(surface)
    pangocairo_context = pangocairo.CairoContext(cairo_context)

    # settings
    pango_layout = pangocairo_context.create_layout()
    pango_layout.set_font_description(font_description)
    pango_layout.set_alignment(pango.ALIGN_CENTER)
    pango_layout.set_width(WIDTH*pango.SCALE)

    # background
    pangocairo_context.set_source_rgb(*BACKGROUND)
    pangocairo_context.rectangle(0, 0, WIDTH, HEIGHT)
    pangocairo_context.fill()

    pangocairo_context.set_source_rgb(*FOREGROUND)
    pango_layout.set_text(text)
    layout_width, layout_height = pango_layout.get_pixel_size()
    ink, logical = pango_layout.get_pixel_extents()
    pangocairo_context.move_to(0, HEIGHT/2 - logical[3]/2)
    pangocairo_context.show_layout(pango_layout)

    surface.write_to_png('%s_pangocairo.png' % filename)

