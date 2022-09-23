#使用Mysql来存储数据。

import json
import sys
from module1 import tse,wSetFileName,urldb
from db_conn import WalletID
import pymysql

path=sys.path[0]
config_file= path+'./config/config.json'
with open(config_file, 'r') as fc_file:
    wconfig = json.load(fc_file)
    print(wconfig)
apikey=wconfig["APIKey"]
dhost=wconfig
#取得钱包的数据。
WalletAdds = WalletID()
for WalletAdd in WalletAdds:

    ethurl = "https://api.etherscan.io/api?module=account&action=tokentx&address="+WalletAdd[2]+"&tag=latest&apikey="+apikey
    wSheetName = WalletAdd[1]

    wtds =urldb(ethurl)
    print("开始读取")
    print(wSheetName)
    wfileName=wSetFileName(wSheetName)
    wresults=wtds["result"]

    for result in wresults:

        wblockNumber= result["blockNumber"]
        whash=result["hash"]   
        wTime = tse(result["timeStamp"])
        wfromWallet = result["from"]
        wcontractAddress = result["contractAddress"]
        wtoWallet = result["to"]
        wValuein=int(result["value"])/1000000
        wtokenName=result["tokenName"]
        wGasfee=int(result["gasUsed"])*int(result["gasPrice"])/1000000000000000000.00
        wgasPrice=result["gasPrice"]
        if wfromWallet == str.lower(WalletAdd[2]):
            wValue=-wValuein
            wStatus="Out"
            
        elif wtoWallet == str.lower(WalletAdd[2]):
            wValue=wValuein
            wStatus="In"
        else:
            wValue=wValuein
            wStatus="Error"      


        sql = "INSERT INTO `transactions` (`transid`,wid,`blockNumber`,`Hash`,`Date`,`FromAdd`,`ContractAddress`,`ToAdd`,`TokenName`,Status,`Value`,`GasFee`,`gasPrice`) VALUES (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(WalletAdd[0],wblockNumber,whash,wTime,wfromWallet,wcontractAddress,wtoWallet,wtokenName,wStatus,wValue,wGasfee,wgasPrice)
        sql_check = "SELECT * FROM `transactions` WHERE `transid`"
        sql_dcheck = "SELECT COUNT(*) FROM `transactions` WHERE `Hash`= '%s'" %(whash)
        print("正在写入钱包的数据,Hash是 %s" %(whash)) 
        print(WalletAdd[2])

        db = pymysql.connect(host='127.0.0.1',port=3306,user='test',password='test',database='test')
        cursor=db.cursor()
        #判断是否已经存在，如果已经存在就跳过，避免因为数据库连接不稳定，重复存储。
        cursor.execute(sql_dcheck)
        infos=cursor.fetchall()
        if infos[0][0] ==0:
            cursor.execute(sql)
            db.commit()
        else:
            print("数据已经存在")

        db.close
        
        
        


print("读取结束")
exit()
