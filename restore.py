import xlrd
import os
import info
import shutil
import dicom
import sys
sys.path.insert(0, "/home/hzzone/caffe/python")
import caffe
import numpy as np
import preprocess

def x2():
    data = xlrd.open_workbook('/Users/HZzone/Desktop/female.xlsx')
    table = data.sheets()[0]
    c = table.col_values(0)
#     test = {'25.00-25.99': 5,
# '22.00-22.99': 11,
# '26.00-26.99': 5,
# '18.00-18.99': 8,
# '24.00-24.99': 6,
# '19.00-19.99': 4,
# '20.00-20.99': 6,
# '21.00-21.99': 8,
# '23.00-23.99': 6,
# '17.00-17.99': 3,
# '14.00-14.99': 2,
# '15.00-15.99': 4}
#     val = {'25.00-25.99': 0,
#             '22.00-22.99': 0,
#             '26.00-26.99': 0,
#             '18.00-18.99': 0,
#             '24.00-24.99': 0,
#             '19.00-19.99': 0,
#             '20.00-20.99': 0,
#             '21.00-21.99': 0,
#             '23.00-23.99': 0,
#             '16.00-16.99': 0,
#             '17.00-17.99': 0,
#             '14.00-14.99': 0,
#             '15.00-15.99': 0}
    test = {'25.00-25.99': 6,
            '16.00-16.99': 2,
            '22.00-22.99': 5,
            '26.00-26.99': 4,
            '18.00-18.99': 3,
            '24.00-24.99': 8,
            '19.00-19.99': 4,
            '20.00-20.99': 3,
            '21.00-21.99': 4,
            '23.00-23.99': 5,
            '17.00-17.99': 1,
            '14.00-14.99': 1}
    val = {'25.00-25.99': 0,
           '22.00-22.99': 0,
           '26.00-26.99': 0,
           '18.00-18.99': 0,
           '24.00-24.99': 0,
           '19.00-19.99': 0,
           '20.00-20.99': 0,
           '21.00-21.99': 0,
           '23.00-23.99': 0,
           '16.00-16.99': 0,
           '17.00-17.99': 0,
           '14.00-14.99': 0,
           '15.00-15.99': 0}
    print c
    for root, dirs, files in os.walk("/Volumes/Hzzone/processed/female"):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            age = info.getInfo(path)
            print age
            n = int(age)
            key = "%.2f-%s" % (n, n + 0.99)
            print key
            for i in c:
                if abs(age-i) <= 0.0000000001:
                    print (age-i)
                    try:
                        if val[key] >= test[key]:
                            continue
                        shutil.move(path, "/Volumes/Hzzone/processed/female/test")
                        val[key] = val[key] + 1
                    except:
                        pass

def x1():
    data = xlrd.open_workbook('/Users/HZzone/Desktop/temp.xlsx')
    table = data.sheets()[0]
    c = table.col_values(0)
    c = [str(x).split('.')[0] for x in c]
    b = []
    for x in c:
        if x.isdigit():
            b.append('0'*(10-len(x)) + x)
        else:
            b.append(x)
    print b
    d = []
    for root, dirs, files in os.walk("/Volumes/SCUHzzone/Bone-Age/data/processed/female"):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            dicom_id = dicom.read_file(path).PatientID
            if dicom_id not in b:
                d.append(dicom_id)
                print dicom_id
                print path
                os.remove(path)
    print len(d)

def number(source):
    rs = {}
    for root, dirs, files in os.walk(source):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            print path
            age = info.getInfo(path)
            a = int(age)
            stage = '%s-%s'%(a, a+1)
            if not rs.has_key(stage):
                rs[stage] = 0
            rs[stage] = rs[stage] + 1

    print rs

def delete(source):
    for root, dirs, files in os.walk(source):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            print path
            age = info.getInfo(path)
            if age<14 or age>28:
                os.remove(path)

def delete1(t1, t2):
    a1 = os.listdir(t1)
    a2 = os.listdir(t2)
    for x in a2:
        if x in a1:
            path = os.path.join(t2, x)
            print path
            os.remove(path)

def x3(caffemodel, deploy, source, mode=True, IMAGE_SIZE=227, LAYER_NAME="my-fc8"):
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
    dic = {}
    for index, result in enumerate(output[LAYER_NAME]):
        predict_age = result[0]
        real_age = real_ages[index]
        file_name = file_list[index]
        id = dicom.read_file(file_list[index]).PatientID
        # only see the error sample
        # if (predict_age > BORDER_AGE and real_age > BORDER_AGE) or (predict_age <= BORDER_AGE and real_age <= BORDER_AGE):
        #     continue
        line = "%s %s %s %s %s" % (file_name, id, real_age, predict_age, abs(predict_age-real_age))
        dic[line] = abs(predict_age - real_age)
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=False)
    test = {'25.00-25.99': 58,
            '16.00-16.99': 27,
            '22.00-22.99': 47,
            '26.00-26.99': 39,
            '18.00-18.99': 27,
            '24.00-24.99': 48,
            '19.00-19.99': 30,
            '20.00-20.99': 34,
            '21.00-21.99': 53,
            '23.00-23.99': 49,
            '27.00-27.99': 3,
            '15.00-15.99': 16,
            '17.00-17.99': 25,
            '14.00-14.99': 18}
    val = {'25.00-25.99': 0,
           '22.00-22.99': 0,
           '26.00-26.99': 0,
           '18.00-18.99': 0,
           '24.00-24.99': 0,
           '19.00-19.99': 0,
           '27.00-27.99': 0,
           '20.00-20.99': 0,
           '21.00-21.99': 0,
           '23.00-23.99': 0,
           '16.00-16.99': 0,
           '17.00-17.99': 0,
           '14.00-14.99': 0,
           '15.00-15.99': 0}
    temp = []
    for key, value in dic:
        # print key, value
        a = key.split(" ")
        n = int(float(a[2]))
        k = "%.2f-%s" % (n, n + 0.99)
        if val[k] < test[k]:
            print key
            val[k] += 1
            temp.append(a[0])

    t1 = set(temp)
    t2 = set(file_list)
    t = t2 - t1
    for x in t:
        os.remove(x)

if __name__ == "__main__":
    # x1()
    # x2()
    # number("/home/hzzone/processed/female/test")
    # number("/home/hzzone/processed/female/train")
    # delete("/home/hzzone/processed/male/train")
    # delete1("/home/hzzone/processed/female/test", "/home/hzzone/processed/female/train")
    # x3(caffemodel="/home/hzzone/1tb/bone-age-model/female/caffenet_train_iter_1200.caffemodel",
    #                           deploy="/home/hzzone/Bone-Age-Assessment/CaffeNet/deploy.prototxt",
    #                           source="/home/hzzone/processed/female/train")
    # number("/home/hzzone/processed/male/test")
    number("/home/hzzone/processed/male/train")


