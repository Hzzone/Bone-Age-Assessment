import dicom
import os
import datetime
import shutil
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
    index = 2000
    for root, dirs, files in os.walk(source):
        for file in files:
            index = index + 1
            os.rename(os.path.join(root, file), os.path.join(root, str(index)+".jpg"))
            # print(os.path.join(root, str(index)+".jpg"))
            # print(len(files))

if __name__ == "__main__":
    # rename("/Volumes/Hzzone-Disk/image/25")
    move("/Volumes/Hzzone-Disk/image/25")

