import os
import dicom
import datetime
import xlrd

def statistic(source):
    f = open("/Users/HZzone/Desktop/test.txt", "w")
    error = open("/Users/HZzone/Desktop/error.txt", "w")
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            try:
                ds = dicom.read_file(path)
            except:
                error.write(path+" ")
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
            f.write(s)
    f.close()
    error.close()
# statistic("/Volumes/Hzzone-Disk/female")
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

if __name__ == "__main__":
    statistic("/Volumes/Hzzone-Disk/backup")

