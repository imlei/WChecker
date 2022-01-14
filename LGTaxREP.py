#对Amazon的GST和PST的信息进行汇总合并，并生成报表。
#如果目录下有多个文件，可以进行选择。

import os
import sys
import csv
import turtle
from unittest import result
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import datetime


#参数设置
#设置转为为Excel的文件名
set_excel_file = "taxreport.xlsx"

#csv 转换成excel文件的模块
def csvtoxlsx(self):
    csv = pd.read_csv(self,encoding='utf-8')
    csv.to_excel(set_excel_file,sheet_name='Sheet1')
#获得当前的工作目录
filePath = sys.path[0]

#filePath = r"C:\Users\yuki\Desktop\tools\LGGST"
os.chdir(filePath)
print("文件夹的地址")
print(filePath)
print("开始遍历")
filecsv = []
for root, dirs, files in os.walk(filePath):

   #cvs to excel,取得文件名
   for file in files:
       if file.endswith(".csv"):
           filecsv.append(file)

#遍历文件，并且选择想要生成的数据。
print("你想选择哪一个文件")
num1 = 0
for csv_file in filecsv:
    
    num1 += 1
    flist = str(num1)+"."+csv_file
    print(flist)

while True:
    choosefile = input("请选择：")
    if int(choosefile) >= num1 :
       print("错误选择,请重选")
    choosefile = input("请选择：")

print("你的选择是",choosefile)
cclist = int(choosefile)-1
ccsv_file = filecsv[cclist]
excelfile = csvtoxlsx(ccsv_file)
print(excelfile)
#读取和操作Excel的文件
dfs = pd.read_excel(set_excel_file)
taxreport = pd.pivot_table(dfs, values="Tax_Amount", index="Tax_Type", aggfunc="sum", margins=True, margins_name="合计")
print("您选择的文件是",ccsv_file)
print(taxreport)
#把生成的数据透视表写入到csv.csv.excel
today = str(datetime.date.today())
path = filePath+"\\"+today+".xlsx"
print(taxreport.sum())
result_sum=pd.DataFrame(taxreport.sum())
#加T有调整调换transpose
#result_sum=pd.DataFrame(taxreport.sum()).T 

result_pivot_sum=taxreport.append(result_sum)
print(result_pivot_sum)
result_sum.to_excel(path)


print("具体报告请查看",path)
#writer = pd.ExcelWriter(path, engine = 'openpyxl')
#taxreport.to_excel(writer, sheet_name = 'x1')
#writer.save()
#writer.close()