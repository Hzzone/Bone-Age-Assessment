import sys
sys.path.insert(0, "/home/bw/code/caffe/python")
import caffe
import numpy as np
import info
import os
import preprocess

# predict the age from a new dicom file by a trained caffemodel and deploy file
def predict(caffemodel, deploy, dicom_file):
    age = info.getInfo(dicom_file)
    im = preprocess.process(dicom_file)
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(1, 3, 227, 227)
    # read a dicom file
    net.blobs['data'].data[...] = im
    output = net.forward()
    predict_age = output['my-fc8'][0][0]
    # return age, predict_age
    print("%s predict: %s real: %s" % (dicom_file, predict_age, age))
'''
The dimension of deploy file must be (the length of test dir, 3, 227, 227)
'''
def predict_dir(caffemodel, deploy, source):
    # f = open("predict.log", "w")
    file_list = []
    correct_num = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
            # f.write(str(real_age)+" "+str(predict_age)+'\n')
    # f.close()
    images = np.zeros((len(file_list), 3, 227, 227), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file)
        # if abs(predict_age - real_age)<=3:
        #     correct_num = correct_num+1
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, 227, 227)
    net.blobs['data'].data[...] = images
    output = net.forward()
    for index, result in enumerate(output['my-fc8']):
        predict_age = result[0]
        real_age = real_ages[index]
        '''
        the condition that you think the prediction result is correct
        '''
        # if abs(predict_age - real_age) <= 3:
        #     correct_num = correct_num+1
        if (predict_age > 18 and real_age > 18) or (predict_age<=18 and real_age<=18):
            correct_num = correct_num+1
    return float(correct_num)/len(file_list)

def predict_by_caffemodel_dir(caffemodel_source, test_deploy, test_data_spurce):
    f = open("predict.log", "w")
    results = {}
    for root, dirs, files in os.walk(caffemodel_source):
        # if out of memory, ten by ten to test
        for index, file in enumerate(files):
            # if index >= 10:
            #     exit(0)
            path = os.path.join(root, file)
            probal = predict_dir(path, test_deploy, test_data_spurce)
            results[path] = probal
    results = sorted(results.items(), key=lambda d: d[1], reverse=True)
    print(results)
    for result in results:
        f.write("%s %f\n" % (result[0], result[1]))
    f.close()

def predict_dir_output(caffemodel, deploy, source):
    # f = open("predict.log", "w")
    file_list = []
    correct_num = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
            # f.write(str(real_age)+" "+str(predict_age)+'\n')
    # f.close()
    images = np.zeros((len(file_list), 3, 227, 227), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file)
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, 227, 227)
    net.blobs['data'].data[...] = images
    output = net.forward()
    for index, result in enumerate(output['my-fc8']):
        predict_age = result[0]
        real_age = real_ages[index]
        '''
        the condition that you think the prediction result is correct
        '''
        print("%s predict: %s real: %s" % (file_list[index], predict_age, real_age))
# run
# print(predict_dir("/home/bw/DeepLearning/male_regression/stepsize, 6000/caffenet_train_iter_1000.caffemodel", "/home/bw/DeepLearning/male_regression/deploy.prototxt", "/home/bw/DeepLearning/male_regression/test"))
predict_by_caffemodel_dir("/home/bw/DeepLearning/male_regression/Caffenet/nodiv256", "/home/bw/DeepLearning/male_regression/Caffenet/test_deploy.prototxt", "/home/bw/DeepLearning/male_regression/test")
# print(predict_dir("/home/bw/DeepLearning/male_regression/stepsize, 6000/caffenet_train_iter_1000.caffemodel", "/home/bw/DeepLearning/male_regression/test_deploy.prototxt", "/home/bw/DeepLearning/male_regression/test"))
# predict_dir_output("/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_2000.caffemodel", "/home/bw/DeepLearning/male_regression/Caffenet/test_deploy.prototxt", "/home/bw/DeepLearning/male_regression/test")
