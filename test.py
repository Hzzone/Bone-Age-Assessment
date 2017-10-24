# -*- coding: utf-8 -*-
import os
import datetime
import dicom
import shutil
import info
def x1(source, target):
	for root, dirs, files in os.walk(source):
		for dicom_file in files:
			path = os.path.join(root, dicom_file)
			ds = dicom.read_file(path)
			birthDate = ds.PatientBirthDate
			studyDate = ds.StudyDate
			bDate = birthDate[0:4] + '-' + birthDate[4:6] + '-' + birthDate[6:8]
			sDate = studyDate[0:4] + '-' + studyDate[4:6] + '-' + studyDate[6:8]
			bd = datetime.datetime.strptime(bDate, '%Y-%m-%d')
			sd = datetime.datetime.strptime(sDate, '%Y-%m-%d')
			days = (sd - bd).days
			age = float(days) / 365.25
			if ds.PatientSex == 'F':
				sex = 'female'
			elif ds.PatientSex == 'M':
				sex = 'male'
			p = os.path.join(target, sex)
			if age<11 or age>=12:
				pass
			else:
				print(path, p)
				shutil.move(path, p)
				pass


def test(source):
    for root, dirs, files in os.walk(source):
        for dicom_file in files:
            path = os.path.join(root, dicom_file)
            age = info.getInfo(path)
            print root, age


if __name__ == "__main__":
	# x1("/Volumes/Hzzone/11/测试集", "/Volumes/Hzzone/11/test")
	# x1("/Volumes/Hzzone/11/训练集", "/Volumes/Hzzone/11/train")
    # print(info.getInfo("/Volumes/Hzzone/补充资料+重新训练10月22日/测试集 二/女性/11（空）/40182985"))
    test("/Volumes/Hzzone/BoneAgeData")
