import os
import dicom
import datetime
import xlrd
import info
import h5py

def statistic(source):
    result = []
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            try:
                ds = dicom.read_file(path)
            except:
                print "error"
            birthDate = ds.PatientBirthDate
            studyDate = ds.StudyDate
            bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
            sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
            bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
            sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
            days = (sd - bd).days
            age = days / 365
            sex = ds.PatientSex
            id = ds.PatientID
            s = "%s %s %s %s %.2f\n" % (id, sex, birthDate, studyDate, age)
            print s
            result.append(s)
    print "complete!"
    return result

def delete(source):
    r = []
    to_delete = xlrd.open_workbook("delete.xlsx")
    table = to_delete.sheets()[0]
    for i in range(table.nrows):
        r.append(str(int(table.row_values(i)[0])))

    for root, dirs, files in os.walk(source):
        for file in files:
                if file in r:
                    path = os.path.join(root, file)
                    print(path)
                    os.remove(path)


def compute(source):
    r = []
    for root, dirs, files in os.walk(source):
        for file in files:
            r.append(file)
    print(len(r))

# the error sample to delete
def error_sample(source):
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            age = info.getInfo(path)
            if age < 14 or age > 27:
                print(path+" " + str(age))

def read_hdf5(source):
    f = h5py.File(source, 'r')
    # print f.keys()
    label = f['label'][:]
    number = len(label)
    result = {}
    for a in label:
        n = int(a)
        key = "%.2f-%s" % (n, n+0.99)
        if not result.has_key(key):
            result[key] = 0
        result[key] = result[key] + 1
    f.close()
    for key in result:
        result[key] = str(result[key])
    result = result.items()
    emmmm = []
    for s in result:
        emmmm.append(" ".join(s))
    emmmm.append(str(number))
    return emmmm

def read_folder(source):
    ages = []
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            try:
                ds = dicom.read_file(path)
            except:
                print "error"
            birthDate = ds.PatientBirthDate
            studyDate = ds.StudyDate
            bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
            sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
            bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
            sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
            days = (sd - bd).days
            age = days / 365
            ages.append(age)
    result = {}
    number = len(ages)
    for a in ages:
        n = int(a)
        key = "%.2f-%s" % (n, n+0.99)
        if not result.has_key(key):
            result[key] = 0
        result[key] = result[key] + 1
    for key in result:
        result[key] = str(result[key])
    result = result.items()
    emmmm = []
    for s in result:
        emmmm.append(" ".join(s))
    emmmm.append(str(number))
    print "complete!"
    return emmmm

if __name__ == "__main__":
    f = open("./paper/data.txt", 'w')
    f.write("male train\n")
    result = read_hdf5("/home/bw/DeepLearning/male_regression/CaffeNet/train.h5")
    f.write("\n".join(result))
    f.write("\n--------------\n")
    f.write("male test\n")
    result = read_folder("/home/bw/DeepLearning/male_regression/test")
    f.write("\n".join(result))
    f.write("\n--------------\n")
    f.write("female train\n")
    result = read_hdf5("/home/bw/DeepLearning/female_regression/CaffeNet/train.h5")
    f.write("\n".join(result))
    f.write("\n--------------\n")
    f.write("female test\n")
    result = read_folder("/home/bw/DeepLearning/female_regression/test")
    f.write("\n".join(result))
    f.close()
