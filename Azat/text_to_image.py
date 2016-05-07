#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
import os
import random

from itertools import chain

from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

# FONTS

def get_random_font():
    fonts_path = r"Fonts/"
    font_list = os.listdir(fonts_path)
    font_path = os.path.join(fonts_path, font_list[random.randint(0, len(font_list) - 1)])
    return font_path

def can_display_text_using_font(text, font_path):
    ttf = TTFont(font_path, 0, verbose=0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)
    chars = chain.from_iterable([y + (Unicode[y[0]],) for y in x.cmap.items()] for x in ttf["cmap"].tables)
    chars = {unichr(x[0]) for x in chars}
    for char in text:
        if unicode(char) not in chars:
            ttf.close()
            return False

    ttf.close()
    return True

def draw_text_using_font(text, font_path):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    image = Image.new("RGBA", (700, 500), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 100)
    draw.text((0, 0), bidi_text, (0, 0, 0), font=font)
    width, height = draw.textsize(bidi_text, font=font)
    image_frames = []
    for i in xrange(len(bidi_text)):
        line = bidi_text[:i + 1]
        symbol = bidi_text[i:i + 1]
        w, _ = draw.textsize(line, font=font)
        line_frame = [(0, 0), (w, height)]
        symbol_width, _ = draw.textsize(symbol, font=font)
        symbol_frame = [(w - symbol_width, 0), (symbol_width, height)]
        image_frames.append({'symbol': symbol,
                             'frame' : symbol_frame})
        draw.rectangle(line_frame, outline=(0, 0, 0))
    return image, image_frames

def text_to_image(text):
    font_path = get_random_font()
    print "Choosed font at path " + font_path
    if can_display_text_using_font(text, font_path):
        return draw_text_using_font(text, font_path)
    else:
        print "Cannot display text using font at path" + font_path
        return None, None

# Example

text = u'اللغة العربية رائعة'
image, frames = text_to_image(text)
if image != None:
    print frames
    image.save("Images/image.png", 'PNG')