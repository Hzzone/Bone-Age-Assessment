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
import predict
if __name__ == "__main__":
    predict.predict("/home/bw/DeepLearning/male_regression/学习率递减，6000/caffenet_train_iter_1000.caffemodel", "/home/bw/DeepLearning/male_regression/deploy.prototxt", "/home/bw/DeepLearning/male_regression/test/31247210")
