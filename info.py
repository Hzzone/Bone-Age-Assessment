import dicom
import datetime

# get the age of one sample from source path
def getInfo(source):
    try:
        ds = dicom.read_file(source)
        birthDate = ds.PatientBirthDate
        studyDate = ds.StudyDate
        bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
        sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
        bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
        sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
        days = (sd - bd).days
        age = float(days) / 365
        return age
    except:
        print(source+" is not a dicom file")

