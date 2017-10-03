import xlrd
import os
import info
import shutil
import dicom

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


if __name__ == "__main__":
    # x1()
    x2()
    # number("/Volumes/Hzzone/processed/male")

