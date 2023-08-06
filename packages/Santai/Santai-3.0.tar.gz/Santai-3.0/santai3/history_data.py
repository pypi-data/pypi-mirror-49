__author__ = 'Administrator'
import tushare as ts
import pandas as pd

data=ts.get_hist_data('000016')
print(data)
data2a = ts.get_h_data('000300') #前复权
print(data2a)

data2 = ts.get_h_data('002337', start='2010-01-15', end='2019-01-01') #两个日期之间的前复权数据
#df = ts.get_today_ticks('601333')
#print(df)

data3 = ts.get_hist_data('sh')#获取上证指数k线数据，其它参数与个股一致，下同
data4 = ts.get_hist_data('sz')#获取深圳成指k线数据
data5 = ts.get_hist_data('hs300')#获取沪深300指数k线数据
data6 = ts.get_hist_data('sz50')#获取上证50指数k线数据
data7 = ts.get_hist_data('zxb')#获取中小板指数k线数据
data8 = ts.get_hist_data('cyb')#获取创业板指数k线数据

#print(data5)
pd.set_option('display.width',1000)
df = ts.get_stock_basics()
date = df.ix['002337']['timeToMarket'] #上市日期YYYYMMDD
#print(df)
#print(date)

df = ts.get_index()
print(data5)
print(df)