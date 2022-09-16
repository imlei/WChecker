import json
import sys
import urllib.request
from module1 import wdataSort,wd2excel,wSetFileName
import pandas as pd
path=sys.path[0]
def WTran(wts):
    response = urllib.request.urlopen(wts)
    WTrans = json.loads(response.read())
    return WTrans
config_file= path+'./config/config.json'
with open(config_file, 'r') as fc_file:
    wconfig = json.load(fc_file)
    print(wconfig)
apikey=wconfig["APIKey"]
WalletAdds=wconfig["WalletAddress"]


for WalletAdd in WalletAdds:
#for i in range(1,100):
    #print(i)
    #WalletAdd=WalletAdds[str(i)]
    #if WalletAdd['Name'] == 'NA':
    #    exit
    #else:

    #print(WalletAdd['Name'],WalletAdd['Address'])
    if WalletAdd['Name'] != "NA":
        ethurl = "https://api.etherscan.io/api?module=account&action=tokentx&address="+WalletAdd['Address']+"&tag=latest&apikey="+apikey
        wSheetName = WalletAdd['Name']

        wtd = WTran(ethurl) 
        print("开始读取")
        print(wSheetName)
        wfileName=wSetFileName(wSheetName)
        walletdata = pd.DataFrame(wdataSort(wtd))
        wd2excel(walletdata,wfileName,wSheetName)
    else:
        print("读取结束")
        exit()
