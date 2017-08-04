from scipy.misc import bytescale
import stastics
import info
import os
import move
import regression
import preprocess
import hdf5
import dicom
from skimage.transform import resize
if __name__ == "__main__":
    # hdf5.generateHdf5("/home/bw/DeepLearning/male_regression/test", "/home/bw/DeepLearning/male_regression/test.h5")
    # hdf5.generateHdf5("/home/bw/DeepLearning/male_regression/male", "/home/bw/DeepLearning/male_regression/train.h5")
    ds = dicom.read_file("/home/bw/DeepLearning/male_regression/male/31246788")
    age = info.getInfo("/home/bw/DeepLearning/male_regression/male/31246788")
    pixel_array = ds.pixel_array
    height, width = pixel_array.shape
    if height < width:
        pixel_array = pixel_array[:, (width - height) / 2:(width + height) / 2]
    else:
        pixel_array = pixel_array[(height - width) / 2:(width + height) / 2, :]
    im = resize(pixel_array, (227, 227))
    im = bytescale(im)
    print(im/256)

