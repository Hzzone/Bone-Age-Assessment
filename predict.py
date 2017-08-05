from __future__ import division
import sys
sys.path.insert(0, "/home/bw/code/caffe/python")
import caffe
import numpy as np
import info
from skimage.transform import resize
from scipy.misc import bytescale
import dicom
import os

# predict the age from a new dicom file by a trained caffemodel and deploy file
def predict(caffemodel, deploy, dicom_file):
    ds = dicom.read_file(dicom_file)
    age = info.getInfo(dicom_file)
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
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(1, 3, 227, 227)
    # read a dicom file
    net.blobs['data'].data[...] = im
    output = net.forward()
    predict_age = output['my-fc8'][0][0]
    return age, predict_age
    # print("predict: %s real: %s" % (predict_age, age))

def predict_dir(caffemodel, deploy, source):
    # f = open("predict.log", "w")
    file_list = []
    correct_num = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
            # f.write(str(real_age)+" "+str(predict_age)+'\n')
    # f.close()
    for dicom_file in file_list:
        real_age, predict_age = predict(caffemodel, deploy, dicom_file)
        if abs(predict_age - real_age)<=3:
            correct_num = correct_num+1
    return float(correct_num)/len(file_list)

def predict_by_caffemodel_dir(source):
    f = open("predict.log", "w")
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            probal = predict_dir(path, "/home/bw/DeepLearning/male_regression/deploy.prototxt", "/home/bw/DeepLearning/male_regression/test")
            f.write("%s %f" % (path, probal))
    f.close()
# run
# print(predict_dir("/home/bw/DeepLearning/male_regression/stepsize, 6000/caffenet_train_iter_1000.caffemodel", "/home/bw/DeepLearning/male_regression/deploy.prototxt", "/home/bw/DeepLearning/male_regression/test"))
predict_by_caffemodel_dir("/home/bw/DeepLearning/male_regression/stepsize, 6000")

