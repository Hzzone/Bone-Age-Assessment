import sys
sys.path.insert(0, "/home/bw/code/caffe/python")
import caffe
import numpy as np
import os
import preprocess
import matplotlib.pyplot as plt
import shutil
from scipy.misc import imsave

# predict the age from a new dicom file by a trained caffemodel and deploy file
def visualize_layers(caffemodel, deploy, dicom_file, IMAGE_SIZE=227):
    im = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(1, 3, IMAGE_SIZE, IMAGE_SIZE)
    # read a dicom file
    net.blobs['data'].data[...] = im
    net.forward()
    curr_path = os.path.dirname(os.path.abspath(__file__))
    # get every layer feature map and save to files
    for layer_name, param in net.params.iteritems():
        features_path = os.path.join(curr_path, layer_name)
        if os.path.exists(features_path):
            shutil.rmtree(features_path)
    LAYER_NAME = "conv1"
    path = "./%s" % LAYER_NAME
    os.mkdir(path)
    features = net.blobs[LAYER_NAME].data[0]
    for index, feature in enumerate(features):
        plt.xticks([])
        plt.yticks([])
        plt.imshow(feature)
        plt.axis('off')
        plt.savefig("%s/%s" % (path, index), bbox_inches='tight', pad_inches=0)
        # plt.show()
    # for layer_name, param in net.params.iteritems():
    #     features_path = os.path.join(curr_path, layer_name)
    #     print net.blobs[layer_name]
        # if layer feature map folder not exists
        # if not os.path.exists(features_path):
        #     os.mkdir(features_path)
        # for index, feature in enumerate(net.blobs[layer_name].data[0]):
        #     path = os.path.join(features_path, str(index))
        #     # plt.imsave(path, feature, cmap=plt.cm.gray)
        #     # plt.imshow(feature)
        #     # plt.show()
        #     # imsave(path+".jpg", feature)
        #     print path
    # full connected layer
    # fc6
    # feat = net.blobs['fc6'].data[0]
    # plt.subplot(2, 1, 1)
    # plt.plot(feat.flat)
    # plt.subplot(2, 1, 2)
    # _ = plt.hist(feat.flat[feat.flat > 0], bins=100)
    # plt.show()
    # fc7
    # feat = net.blobs['fc7'].data[0]
    # plt.subplot(2, 1, 1)
    # plt.plot(feat.flat)
    # plt.subplot(2, 1, 2)
    # _ = plt.hist(feat.flat[feat.flat > 0], bins=100)
    # plt.show()
    # fc8
    # feat = net.blobs['my-fc8'].data[0]
    # plt.subplot(2, 1, 1)
    # plt.plot(feat.flat)
    # plt.subplot(2, 1, 2)
    # _ = plt.hist(feat.flat[feat.flat > 0], bins=100)
    # plt.show()


def vis_square(data):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""

    # normalize data for display

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
                (0, 1), (0, 1))  # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    plt.imshow(data)
    plt.axis('off')
    plt.show()

if __name__=="__main__":
    visualize_layers("/home/bw/DeepLearning/male_regression/CaffeNet/model/caffenet_train_iter_2000.caffemodel",
                     "/home/bw/DeepLearning/male_regression/CaffeNet/deploy.prototxt",
                     "/home/bw/DeepLearning/male_regression/test/33660437")
