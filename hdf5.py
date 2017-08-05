import h5py as hy
import os
import dicom
import info
import random
import shutil
from skimage.transform import resize
import numpy as np
from scipy.misc import imsave
from scipy.misc import bytescale

def generateHdf5(source, target):
    h5_file = hy.File(target, 'w')
    file_list = []
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
    random.shuffle(file_list)
    random.shuffle(file_list)
    data = np.zeros((len(file_list), 3, 227, 227), dtype=np.float)
    labels = np.zeros(len(file_list), dtype=np.float32)
    for index, file in enumerate(file_list):
        ds = dicom.read_file(file)
        age = info.getInfo(file)
        pixel_array = ds.pixel_array
        height, width = pixel_array.shape
        if height < width:
            pixel_array = pixel_array[:, int((width - height) / 2):int((width + height) / 2)]
        else:
            pixel_array = pixel_array[int((height - width) / 2):int((width + height) / 2), :]
        im = resize(pixel_array, (227, 227))
        im = bytescale(im)
        im = im/256
        im = np.dstack((im, im, im))
        im = im[:, :, [2, 1, 0]]
        im = im.transpose((2, 0, 1))
        data[index, :, :, :] = im
        labels[index] = age
        print(os.path.join(root, file))
    h5_file['data'] = data
    h5_file['label'] = labels

    print(labels)
    h5_file.close()
