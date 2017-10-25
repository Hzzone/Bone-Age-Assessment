import sys
sys.path.insert(0, "/home/hzzone/caffe/python")
import caffe
import numpy as np
import info
import os
import preprocess
import dicom

# predict the age from a new dicom file by a trained caffemodel and deploy file
def predict(caffemodel, deploy, dicom_file, IMAGE_SIZE=227, LAYER_NAME="my-fc8"):
    age = info.getInfo(dicom_file)
    im = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(1, 3, IMAGE_SIZE, IMAGE_SIZE)
    # read a dicom file
    net.blobs['data'].data[...] = im
    output = net.forward()
    predict_age = output[LAYER_NAME][0][0]
    # return age, predict_age
    print("%s predict: %s real: %s" % (dicom_file, predict_age, age))
'''
The dimension of deploy file must be (the length of test dir, 3, 227, 227)
'''
def predict_dir(caffemodel, deploy, source, IMAGE_SIZE=227, LAYER_NAME="my-fc8", mode=True, BORDER_AGE=18):
    # f = open("predict.log", "w")
    file_list = []
    correct_num = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
            # f.write(str(real_age)+" "+str(predict_age)+'\n')
    # f.close()
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
        # if abs(predict_age - real_age)<=3:
        #     correct_num = correct_num+1
    if mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE)
    net.blobs['data'].data[...] = images
    output = net.forward()
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        '''
        the condition that you think the prediction result is correct
        '''
        # if abs(predict_age - real_age) <= 3:
        #     correct_num = correct_num+1
        if (predict_age > BORDER_AGE and real_age > BORDER_AGE) or (predict_age <= BORDER_AGE and real_age <= BORDER_AGE):
            correct_num = correct_num+1
    return float(correct_num)/len(file_list)

def predict_by_caffemodel_dir(caffemodel_source, test_deploy, test_data_source, IMAGE_SIZE=227, mode=True, LAYER_NAME="my-fc8", LOG_FILE="predict_log"):
    f = open(LOG_FILE, "w")
    results = {}
    for root, dirs, files in os.walk(caffemodel_source):
        # if out of memory, ten by ten to test
        for index, file in enumerate(files):
            # if index >= 10:
            #     exit(0)
            path = os.path.join(root, file)
            probal = predict_dir(caffemodel=path, deploy=test_deploy, source=test_data_source, IMAGE_SIZE=IMAGE_SIZE, mode=mode, LAYER_NAME=LAYER_NAME)
            results[path] = probal
    results = sorted(results.items(), key=lambda d: d[1], reverse=True)
    print(results)
    for result in results:
        f.write("%s %f\n" % (result[0], result[1]))
    f.close()

def predict_dir_output(caffemodel, deploy, source, mode=True, IMAGE_SIZE=227, LAYER_NAME="my-fc8", LOGFILE="predict.log", BORDER_AGE=18):
    # f = open("predict.log", "w")
    file_list = []
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file)
    if mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE)
    net.blobs['data'].data[...] = images
    output = net.forward()
    f = open(LOGFILE, 'w')
    dic = {}
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        # only see the error sample
        # if (predict_age > BORDER_AGE and real_age > BORDER_AGE) or (predict_age <= BORDER_AGE and real_age <= BORDER_AGE):
        #     continue
        line = "%s %s %s" % (real_age, predict_age, abs(predict_age - real_age))
        dic[line] = abs(predict_age - real_age)
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for key, value in dic:
        f.write("%s\n" % key)
        # print(type(dic[key]))
        # print(key, value)
    f.close()


def predict_dir_output_temp(caffemodel, deploy, source, mode=True, IMAGE_SIZE=227, LAYER_NAME="my-fc8", LOGFILE="predict.log", BORDER_AGE=18):
    # f = open("predict.log", "w")
    file_list = []
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file)
    if mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE)
    net.blobs['data'].data[...] = images
    output = net.forward()
    f = open(LOGFILE, 'w')
    dic = {}
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
	file_name = file_list[index]
        # only see the error sample
        # if (predict_age > BORDER_AGE and real_age > BORDER_AGE) or (predict_age <= BORDER_AGE and real_age <= BORDER_AGE):
        #     continue
        line = "%s %s" % (file_name.split('/')[-1], predict_age)
        dic[line] = abs(predict_age - real_age)
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for key, value in dic:
        f.write("%s\n" % key)
        # print(type(dic[key]))
        # print(key, value)
    f.close()

def predict_dir_output_temp_1(caffemodel, deploy, source, mode=True, IMAGE_SIZE=227, LAYER_NAME="my-fc8", LOGFILE="predict.log", BORDER_AGE=18):
    # f = open("predict.log", "w")
    file_list = []
    for root, dirs, files in os.walk(source):
        for file in files:
            file_list.append(os.path.join(root, file))
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file)
    if mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE)
    net.blobs['data'].data[...] = images
    output = net.forward()
    f = open(LOGFILE, 'w')
    dic = {}
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        file_name = file_list[index]
        id = dicom.read_file(file_list[index]).PatientID
        # only see the error sample
        # if (predict_age > BORDER_AGE and real_age > BORDER_AGE) or (predict_age <= BORDER_AGE and real_age <= BORDER_AGE):
        #     continue
        line = "%s %s %s %s %s" % (file_name.split('/')[-1], id, real_age, predict_age, abs(predict_age-real_age))
        dic[line] = abs(predict_age - real_age)
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for key, value in dic:
        f.write("%s\n" % key)
        # print(type(dic[key]))
        # print(key, value)
    f.close()
# run

# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/female_regression/GoogLeNet/model", test_deploy="/home/bw/DeepLearning/female_regression/GoogLeNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/female_regression/test", IMAGE_SIZE=224, mode=False, LOG_FILE="GoogLeNet_predict.log", LAYER_NAME="my-loss3/classifier")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/female_regression/ResNet50/model", test_deploy="/home/bw/DeepLearning/female_regression/ResNet50/deploy.prototxt", test_data_source="/home/bw/DeepLearning/female_regression/test", IMAGE_SIZE=224, mode=False, LOG_FILE="ResNet_predict.log", LAYER_NAME="my-score")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/female_regression/CaffeNet/model", test_deploy="/home/bw/DeepLearning/female_regression/CaffeNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/female_regression/test", LOG_FILE="CaffeNet_predict.log")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/female_regression/AlexNet/model", test_deploy="/home/bw/DeepLearning/female_regression/AlexNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/female_regression/test", LOG_FILE="AlexNet_predict.log")

# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/male_regression/GoogLeNet/model", test_deploy="/home/bw/DeepLearning/male_regression/GoogLeNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/male_regression/test", IMAGE_SIZE=224, mode=False, LOG_FILE="GoogLeNet_predict.log", LAYER_NAME="my-loss3/classifier")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/male_regression/ResNet50/model", test_deploy="/home/bw/DeepLearning/male_regression/ResNet50/deploy.prototxt", test_data_source="/home/bw/DeepLearning/male_regression/test", IMAGE_SIZE=224, mode=False, LOG_FILE="ResNet_predict.log", LAYER_NAME="my-score")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/male_regression/CaffeNet/model", test_deploy="/home/bw/DeepLearning/male_regression/CaffeNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/male_regression/test", LOG_FILE="CaffeNet_predict.log")
# predict_by_caffemodel_dir(caffemodel_source="/home/bw/DeepLearning/male_regression/AlexNet/model", test_deploy="/home/bw/DeepLearning/male_regression/AlexNet/deploy.prototxt", test_data_source="/home/bw/DeepLearning/male_regression/test", LOG_FILE="AlexNet_predict.log")

# predict_dir_output(caffemodel="/home/bw/DeepLearning/male_regression/CaffeNet/model/caffenet_train_iter_2000.caffemodel", deploy="/home/bw/DeepLearning/male_regression/CaffeNet/deploy.prototxt", source="/home/bw/DeepLearning/male_regression/test", LOGFILE="error.log")
# predict_dir_output(caffemodel="/home/bw/DeepLearning/female_regression/CaffeNet/model/caffenet_train_iter_2000.caffemodel", deploy="/home/bw/DeepLearning/female_regression/CaffeNet/deploy.prototxt", source="/home/bw/DeepLearning/female_regression/test", LOGFILE="error.log")
# predict_by_caffemodel_dir(caffemodel_source="/home/hzzone/1tb/bone-age-model/female", test_deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", test_data_source="/home/hzzone/temp/female", LOG_FILE="female_predict.log")
# predict_by_caffemodel_dir(caffemodel_source="/home/hzzone/1tb/bone-age-model/male", test_deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", test_data_source="/home/hzzone/temp/male", LOG_FILE="male_predict.log")
# predict_dir_output_temp(caffemodel="/home/hzzone/1tb/bone-age-model/female/caffenet_train_iter_1200.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/temp/female", LOGFILE="female_error.log")
# predict_dir_output_temp(caffemodel="/home/hzzone/1tb/bone-age-model/male/caffenet_train_iter_2500.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/temp/male", LOGFILE="male_error.log")
# predict_dir_output_temp_1(caffemodel="/home/hzzone/1tb/bone-age-model/female/caffenet_train_iter_1200.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/female/test", LOGFILE="female_test.log")
predict_dir_output_temp_1(caffemodel="/home/hzzone/1tb/bone-age-model/male/caffenet_train_iter_2500.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/male/test", LOGFILE="male_test.log")
# predict_dir_output_temp_1(caffemodel="/home/hzzone/1tb/bone-age-model/female/caffenet_train_iter_1200.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/female/train", LOGFILE="female_train.log")
predict_dir_output_temp_1(caffemodel="/home/hzzone/1tb/bone-age-model/male/caffenet_train_iter_2500.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/male/train", LOGFILE="male_train.log")

# print predict_dir(caffemodel="/home/hzzone/1tb/bone-age-model/female/caffenet_train_iter_1200.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/female/test", IMAGE_SIZE=227, LAYER_NAME="my-fc8", mode=True, BORDER_AGE=18)
print predict_dir(caffemodel="/home/hzzone/1tb/bone-age-model/male/caffenet_train_iter_2500.caffemodel", deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt", source="/home/hzzone/processed/male/test", IMAGE_SIZE=227, LAYER_NAME="my-fc8", mode=True, BORDER_AGE=18)
