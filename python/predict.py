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
def predict_dir(caffemodel, deploy, file_list, IMAGE_SIZE=227, LAYER_NAME="my-fc8", mode=True):
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        print dicom_file
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
    if mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
    net.blobs['data'].reshape(len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE)
    net.blobs['data'].data[...] = images
    output = net.forward()
    MAE_SUM = 0.0
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        '''
        the condition that you think the prediction result is correct
        '''
        MAE_SUM += abs(predict_age-real_age)
        print(abs(predict_age-real_age))
    print MAE_SUM
    return MAE_SUM/len(file_list)

def predict_by_caffemodel_dir(caffemodel_source, test_deploy, test_data_source_list, IMAGE_SIZE=227, mode=True, LAYER_NAME="my-fc8", LOG_FILE="predict.log"):
    f = open(LOG_FILE, "w")
    results = {}
    for root, dirs, files in os.walk(caffemodel_source):
        # if out of memory, ten by ten to test
        for index, file in enumerate(files):
            path = os.path.join(root, file)
            probal = predict_dir(caffemodel=path, deploy=test_deploy, file_list=test_data_source_list, IMAGE_SIZE=IMAGE_SIZE, mode=mode, LAYER_NAME=LAYER_NAME)
            results[path] = probal
    results = sorted(results.items(), key=lambda d: d[1], reverse=True)
    print(results)
    for result in results:
        f.write("%s %f\n" % (result[0], result[1]))
    f.close()

def predict_dir_output_temp_1(caffemodel, deploy, source_list, mode=True, IMAGE_SIZE=227, LAYER_NAME="my-fc8", LOGFILE="predict.log"):
    images = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE), dtype=np.float)

    # read age list
    real_ages = []
    for index, dicom_file in enumerate(file_list):
        real_age = info.getInfo(dicom_file)
        real_ages.append(real_age)
        images[index, :, :, :] = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
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
    MAE_SUM = 0.0
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        file_name = file_list[index]
        ds = dicom.read_file(file_list[index])
        id = ds.PatientID
        birthDate = ds.PatientBirthDate
        studyDate = ds.StudyDate
        line = "%s %s %s %s %s %s %s" % (file_name.split('/')[-1], id, birthDate, studyDate, real_age, predict_age, abs(predict_age-real_age))
        dic[line] = abs(predict_age - real_age)
        MAE_SUM += abs(predict_age - real_age)
        print(abs(predict_age-real_age))
    f.write("%s\n" % str(MAE_SUM/len(file_list)))
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for key, value in dic:
        f.write("%s\n" % key)
        print(key)
    f.close()
    
    
if __name__ == "__main__":
    file_list = []
    for root, dirs, files in os.walk("/home/hzzone/Bone-Age-Data/test"):
            for file in files:
                file_list.append(os.path.join(root, file))
	
    predict_by_caffemodel_dir("/home/hzzone/1tb/Bone-Age-AlexNet-4096/model", "/home/hzzone/1tb/Bone-Age-AlexNet-4096/alexnet_deploy.prototxt", file_list, LOG_FILE="1.log")
    # predict_by_caffemodel_dir("/home/hzzone/1tb/Bone-Age-AlexNet-2048-2048/model", "/home/hzzone/1tb/Bone-Age-AlexNet-2048-2048/alexnet_deploy.prototxt", file_list, LOG_FILE="2.log")
    # predict_by_caffemodel_dir("/home/hzzone/1tb/Bone-Age-AlexNet-4096-4096/model", "/home/hzzone/1tb/Bone-Age-AlexNet-4096-4096/alexnet_deploy.prototxt", file_list, LOG_FILE="3.log")
    # predict_dir_output_temp_1("/home/hzzone/1tb/Bone-Age-AlexNet-4096/model/all_alexnet_train_iter_100.caffemodel", "/home/hzzone/1tb/Bone-Age-AlexNet-4096/alexnet_deploy.prototxt", file_list)
