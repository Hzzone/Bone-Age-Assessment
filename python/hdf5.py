import h5py as hy
import os
import info
import random
import numpy as np
import preprocess

def generateHdf5(source, target):
    h5_file = hy.File(target, 'w')
    file_list = []
    for root, dirs, files in os.walk(source):
        for dicom_file in files:
            file_list.append(os.path.join(root, dicom_file))
    random.shuffle(file_list)
    random.shuffle(file_list)
    # change the image size to you want
    data = np.zeros((len(file_list), 3, 227, 227))
    labels = np.zeros(len(file_list), dtype=np.float32)
    for index, dicom_file in enumerate(file_list):
        age = info.getInfo(dicom_file)
        im = preprocess.process(dicom_file)
        data[index, :, :, :] = im
        labels[index] = age
        print(dicom_file)
    h5_file['data'] = data
    h5_file['label'] = labels

    print(labels)
    h5_file.close()

def generateHdf5_fromfilelist(source_list, target):
    h5_file = hy.File(target, 'w')
    file_list = []
    for source in source_list:
        for root, dirs, files in os.walk(source):
            for dicom_file in files:
                file_list.append(os.path.join(root, dicom_file))
    random.shuffle(file_list)
    random.shuffle(file_list)
    random.shuffle(file_list)
    # change the image size to you want
    IMAGE_SIZE = 224
    data = np.zeros((len(file_list), 3, IMAGE_SIZE, IMAGE_SIZE))
    labels = np.zeros(len(file_list), dtype=np.float32)
    for index, dicom_file in enumerate(file_list):
        age = info.getInfo(dicom_file)
        im = preprocess.process(dicom_file, IMAGE_SIZE=IMAGE_SIZE)
        data[index, :, :, :] = im
        labels[index] = age
        print(dicom_file, age)
    h5_file['data'] = data
    h5_file['label'] = labels

    print(labels)
    h5_file.close()

if __name__ == "__main__":
    # # all train and test
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train", "/Volumes/Hzzone/BoneAgeData/new_data_train"], "/Volumes/Hzzone/BoneAgeData/224/all/train.h5")
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1", "/Volumes/Hzzone/BoneAgeData/test2"], "/Volumes/Hzzone/BoneAgeData/224/all/test.h5")
    # female and male train and test
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train/female", "/Volumes/Hzzone/BoneAgeData/new_data_train/female"], "/Volumes/Hzzone/BoneAgeData/224/bysex/female_train.h5")
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1/female", "/Volumes/Hzzone/BoneAgeData/test2/female"], "/Volumes/Hzzone/BoneAgeData/224/bysex/female_test.h5")
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train/male", "/Volumes/Hzzone/BoneAgeData/new_data_train/male"], "/Volumes/Hzzone/BoneAgeData/224/bysex/male_train.h5")
    generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1/male", "/Volumes/Hzzone/BoneAgeData/test2/male"], "/Volumes/Hzzone/BoneAgeData/224/bysex/male_test.h5")


    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train", "/Volumes/Hzzone/BoneAgeData/new_data_train"], "/Volumes/Hzzone/BoneAgeData/227/all/train.h5")
    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1", "/Volumes/Hzzone/BoneAgeData/test2"], "/Volumes/Hzzone/BoneAgeData/227/all/test.h5")
    # # female and male train and test
    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train/female", "/Volumes/Hzzone/BoneAgeData/new_data_train/female"], "/Volumes/Hzzone/BoneAgeData/227/bysex/female_train.h5")
    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1/female", "/Volumes/Hzzone/BoneAgeData/test2/female"], "/Volumes/Hzzone/BoneAgeData/227/bysex/female_test.h5")
    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/initial_data_train/male", "/Volumes/Hzzone/BoneAgeData/new_data_train/male"], "/Volumes/Hzzone/BoneAgeData/227/bysex/male_train.h5")
    # generateHdf5_fromfilelist(["/Volumes/Hzzone/BoneAgeData/test1/male", "/Volumes/Hzzone/BoneAgeData/test2/male"], "/Volumes/Hzzone/BoneAgeData/227/bysex/male_test.h5")
