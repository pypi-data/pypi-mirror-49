import tushare as ts
import pandas as pd

def get_all_stock():
    stock_info = ts.get_stock_basics()
    stock_info.to_csv("D:\\test11.csv", encoding="gbk", index=True)
    normal_stocks = stock_info.loc[:,['name']]
    print(normal_stocks)
    tms = pd.read_csv('E:\\stock_data\\terminated_stock.csv', dtype=str, encoding="gbk")
    print(tms)
    print(list(tms.code))
    #delset = tms.loc[:,['code']]
    ks = normal_stocks.drop(list(tms.code))
    print(ks)
    # for row in stock_info.itertuples(index=True, name='Pandas'):
    #     print(row)
    # return  stock_info
get_all_stock()
#print(ts.get_terminated())
# print(ts.get_hs300s())
#
# hs3 = ts.get_hs300s()
# hs4 = hs3.loc[:,['code','name']]
# print(hs4)
# hs4.to_csv("D:\\test300.csv", encoding="gbk", index=False)
#
# hs5 = pd.read_csv('D:\\test300.csv', dtype=str,encoding="gbk")
#
# print(hs5)