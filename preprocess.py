import os
from PIL import Image


def resize(source):
    img = Image.open(source)
    w, h = img.size
    x1=0
    x2=0
    y1=0
    y2=0
    if w > h:
        x1 = (w-h)/2
        x2 = (w+h)/2
        y1 = 0
        y2 = h
    else:
        x1 = 0
        x2 = w
        y1 = (h-w)/2
        y2 = (h+w)/2
    box = (x1, y1, x2, y2)
    img = img.crop(box)
    img = img.resize((227, 227), Image.ANTIALIAS)
    img.save(source)


