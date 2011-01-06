#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont


to_render = [
    ('pl', 'zażółć gęślą jaźń'),
    ('ar', 'مَقْلُوب رَاسًا على عَقْبٍ'),
]

WIDTH = 375
HEIGHT = 50

FOREGROUND = (0, 0, 0)
BACKGROUND = (255, 255, 255)


font_path = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'
font = ImageFont.truetype(font_path, 32, encoding='unic')

for filename, text in to_render:
    text = text.decode('utf-8')
    (width, height) = font.getsize(text)
    image = Image.new('RGBA', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.text(((WIDTH - width)/2, (HEIGHT - height)/2), 
              text, font=font, fill=FOREGROUND)
    image.save('%s_PIL.jpg' % filename)

