# from __future__ import division
import dicom
import numpy as np
from scipy.misc import bytescale
import cv2
import sys

def process(source, IMAGE_SIZE=224):
    ds = dicom.read_file(source)
    pixel_array = ds.pixel_array
    height, width = pixel_array.shape
    if height < width:
        pixel_array = pixel_array[:, int((width - height) / 2):int((width + height) / 2)]
    else:
        pixel_array = pixel_array[int((height - width) / 2):int((width + height) / 2), :]
    im = cv2.resize(pixel_array, (IMAGE_SIZE, IMAGE_SIZE))
    im = bytescale(im)
    # im = im / 256
    im = np.dstack((im, im, im))
    im = im[:, :, [2, 1, 0]]
    im = im.transpose((2, 0, 1))
    return im
