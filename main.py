from scipy.misc import bytescale
import stastics
import info
import os
import move
import regression
import preprocess
import h5py
import dicom
import hdf5
from skimage.transform import resize
if __name__ == "__main__":
    hdf5.generateHdf5("/Volumes/Hzzone-Disk/male_regression/test", "/Volumes/Hzzone-Disk/male_regression/test.h5")
    hdf5.generateHdf5("/Volumes/Hzzone-Disk/male_regression/male", "/Volumes/Hzzone-Disk/male_regression/train.h5")
    # ds = dicom.read_file("/Volumes/Hzzone-Disk/male_regression/male/31246788")
    # age = info.getInfo("/Volumes/Hzzone-Disk/male_regression/male/31246788")
    # pixel_array = ds.pixel_array
    # height, width = pixel_array.shape
    # if height < width:
    #     pixel_array = pixel_array[:, int((width - height) / 2):int((width + height) / 2)]
    # else:
    #     pixel_array = pixel_array[int((height - width) / 2):int((width + height) / 2), :]
    # im = resize(pixel_array, (227, 227))
    # im = bytescale(im)
    # print(im/256)

