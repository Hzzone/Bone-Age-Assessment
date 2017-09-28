import xlrd
import os
data = xlrd.open_workbook('/Users/HZzone/Desktop/remove.xlsx')
table = data.sheets()[0]
c = table.col_values(0)
c = [str(int(x)) for x in c]
for root, dirs, files in os.walk("/Volumes/SCUHzzone/Bone-Age/data/processed"):
    print root
    for dicom_file in files:
        print dicom_file
        if dicom_file in c:
            os.remove(os.path.join(root, dicom_file))
            print dicom_file

