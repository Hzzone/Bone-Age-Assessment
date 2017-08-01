import os
import dicom
import datetime

def statistic(source):
    r = {}
    for root, dirs, files in os.walk(source):
        for file in files:
            ds = dicom.read_file(os.path.join(root, file))
            birthDate = ds.PatientBirthDate
            studyDate = ds.StudyDate
            bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
            sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
            bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
            sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
            days = (sd - bd).days
            age = int(round(days / 365))
            if age not in r.keys():
                r[age] = 0
            r[age] = r[age]+1
            print(file)
    f = open("/Users/HZzone/Desktop/test1.txt", 'w')
    print(r)
    for x in r:
        f.write(str(x)+" "+str(r[x])+'\n')
    f.close()
statistic("/Volumes/Hzzone-Disk/female")
