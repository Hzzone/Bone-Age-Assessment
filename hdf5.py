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
        for file in files:
            file_list.append(os.path.join(root, file))
    random.shuffle(file_list)
    random.shuffle(file_list)
    # change the image size to you want
    data = np.zeros((len(file_list), 3, 227, 227))
    labels = np.zeros(len(file_list), dtype=np.float32)
    for index, file in enumerate(file_list):
        age = info.getInfo(file)
        im = preprocess.process(file)
        data[index, :, :, :] = im
        labels[index] = age
        print(file)
    h5_file['data'] = data
    h5_file['label'] = labels

    print(labels)
    h5_file.close()

if __name__ == "__main__":
    generateHdf5("/Volumes/Hzzone/processed/male/test", "/Volumes/Hzzone/processed/male/test.h5")
    generateHdf5("/Volumes/Hzzone/processed/male/train", "/Volumes/Hzzone/processed/male/train.h5")
    generateHdf5("/Volumes/Hzzone/processed/female/test", "/Volumes/Hzzone/processed/female/test.h5")
    generateHdf5("/Volumes/Hzzone/processed/female/train", "/Volumes/Hzzone/processed/female/train.h5")
