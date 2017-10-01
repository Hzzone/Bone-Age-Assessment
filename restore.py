import xlrd
import os
import info
import shutil
import dicom
def x2():
    data = xlrd.open_workbook('/Users/HZzone/Desktop/female.xlsx')
    table = data.sheets()[0]
    c = table.col_values(0)
    print c
    for root, dirs, files in os.walk("/Volumes/SCUHzzone/Bone-Age/data/processed/female"):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            age = info.getInfo(path)
            print age
            for i in c:
                if abs(age-i) <= 0.0000000001:
                    print (age-i)
                    try:
                        shutil.move(path, "/Volumes/SCUHzzone/Bone-Age/data/processed/female/test")
                    except:
                        continue
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


if __name__ == "__main__":
    # x1()
    x2()

