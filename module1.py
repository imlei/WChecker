from csv import writer
from fileinput import filename
import time
import sys
import time
import os
from openpyxl import load_workbook
import pandas as pd
import urllib.request
import json
path=sys.path[0]
#转换时间戳
def tse(timeStamp):
    now = int(timeStamp)
    timeArray = time.localtime(now)
    timedata = time.strftime("%Y-%m-%d",timeArray)
    return timedata

#运行爬虫，抓取数据
def urldb(tws):
    res=urllib.request.urlopen(tws)
    reader = json.loads(res.read())
    return reader
#对数据进行整理
def wdataSort(walletinfo):
    wdata = []
    wdata.append(["blockNumber","Hash","Time","From","Contract Address","To","Value","Token Name","Gasfee","Gas Price"])
    results=walletinfo['result']
    for result in results:
        wblockNumber= result["blockNumber"]
        whash=result["hash"]   
        wTime = tse(result["timeStamp"])
        wfromWallet = result["from"]
        wcontractAddress = result["contractAddress"]
        wtoWallet = result["to"]
        wValue=int(result["value"])/1000000
        wtokenName=result["tokenName"]
        wGasfee=int(result["gasUsed"])*int(result["gasPrice"])/1000000000000000000.00
        wgasPrice=result["gasPrice"]
        wdata.append([wblockNumber,whash,wTime,wfromWallet,wcontractAddress,wtoWallet,wValue,wtokenName,wGasfee,wgasPrice])
    return wdata

#写入数据到Excel表格
def wd2excel(data,fileName,SheetName):


    #判断文件是否已经存在了，如果不存在，就创建文件。
    if not os.path.exists(fileName):
        writer = fileName
        data.to_excel(writer,sheet_name=SheetName,header=None)
        

    else:
        #writer.book = book
        #data.to_excel(writer,sheet_name=SheetName,header=None)
        print("文件已经存在")
        exit()



#获得文件名
def wSetFileName(SheetName):
    filedate=time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = SheetName+"transations"+filedate+".xlsx"
    datafile = path+r"\\"+filename
    return(datafile)
