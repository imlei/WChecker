#整合各个功能
from ethpricelist import read_price, checkprice

print('今天您想做什么：')
print('1.读取ETH的价格。\n2.查询ETH的历史价格\n')
ans=input('请输入你的选项：')
if ans == "1":
    res = read_price()
if ans == "2":
    date_info = input("请输入你要选择的查询的时间,格式是YYYY-MM-DD")
    res = checkprice(date_info)
    print(res)
else:
    print("error")
