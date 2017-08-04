import os
import dicom
import info
import random
import shutil
from skimage.transform import resize
import numpy as np
from scipy.misc import imsave
from scipy.misc import bytescale

def generateFile(source, target=None):
    f = open(target, 'w')
    for root, dirs, files in os.walk(source):
        for file in files:
            age = info.getInfo(os.path.join(root, file))
            s = "/home/shared/male_regression/png/test/%s.jpg %.2f\n" % (file, age)
            print(s)
            f.write(s)
    f.close()

def moveRegressionTestFile(source):
    f = []
    for root, dirs, files in os.walk(source):
        for file in files:
            f.append(os.path.join(root, file))
    random.shuffle(f)
    random.shuffle(f)
    for index, file in enumerate(f):
        if index % 10 == 0:
            shutil.move(file, "/home/bw/DeepLearning/male_regression/test")
            print(file)

def generateColorImage(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            ds = dicom.read_file(os.path.join(root, file))
            pixel_array = ds.pixel_array
            im = resize(pixel_array, (227, 227))
            # im = bytescale(im)
            im = np.dstack((im, im, im))
            imsave(os.path.join(target, file+'.jpg'), im)
            print(os.path.join(root, file))
