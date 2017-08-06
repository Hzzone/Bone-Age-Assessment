from __future__ import division
import dicom
import numpy as np
from skimage.transform import resize
from scipy.misc import bytescale

def process(source):
    ds = dicom.read_file(source)
    pixel_array = ds.pixel_array
    height, width = pixel_array.shape
    if height < width:
        pixel_array = pixel_array[:, int((width - height) / 2):int((width + height) / 2)]
    else:
        pixel_array = pixel_array[int((height - width) / 2):int((width + height) / 2), :]
    im = resize(pixel_array, (227, 227))
    im = bytescale(im)
    im = im / 256
    im = np.dstack((im, im, im))
    im = im[:, :, [2, 1, 0]]
    im = im.transpose((2, 0, 1))
    return im
