import dicom
import os
import datetime
import shutil
import info
# for root, dirs, files in os.walk("/Volumes/Hzzone-Disk/18"):
#     for file in files:
#         if os.path.isdir(os.path.join(root, file)):
#             continue
#         ds = dicom.read_file(os.path.join(root, file))
#         birthDate = ds.PatientBirthDate
#         studyDate = ds.StudyDate
#         bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
#         sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
#         bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
#         sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
#         days = (sd - bd).days
#         age = int(round(days / 365))
#         print(age)
#         # shutil.move(os.path.join(root, file), "/Volumes/Hzzone-Disk/"+str(age))

def move(source):
    for root, dirs, files in os.walk(source):
        for file in files:
            shutil.move(os.path.join(root, file), source)
        # for d in dirs:
        #     os.remove(os.path.join(root, d))
            # print(os.path.join(root, d))

def rename(source):
    index = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            index = index + 1
            os.rename(os.path.join(root, file), os.path.join(root, str(index)+".jpg"))
            # print(os.path.join(root, str(index)+".jpg"))
            # print(len(files))

# move file to 2 classify problem
def move2(source):
    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)
            age = info.getInfo(path)
            if age > 18:
                shutil.move(path, os.path.join(source, '1'))
            else:
                shutil.move(path, os.path.join(source, '0'))
            print(path)

def move3(source):
    for root, dirs, files in os.walk(source):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            sex = dicom_file[-1]
            if sex == 'F':
                shutil.copy(path, os.path.join("/Volumes/Hzzone/temp", 'female'))
                print sex
                print path
            else:
                shutil.copy(path, os.path.join("/Volumes/Hzzone/temp", 'male'))

if __name__ == "__main__":
    move3("/Volumes/Hzzone/test-9-20")