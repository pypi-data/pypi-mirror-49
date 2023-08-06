__author__ = 'Administrator'

import pandas as pd
from pandas import Series,DataFrame

from sqlalchemy import create_engine
import tushare as ts


import pymysql
pymysql.install_as_MySQLdb()

stocknum='002312'
date='2018-05-09'
df = ts.get_tick_data(stocknum, date)
print(df)

df["date"]=date
df["stocknum"]=stocknum

ser = df["time"]


def toTimeStamp(date,ser):#计算df的时间戳
    """""""""
    print(ser.at[0])
    #print(ser.iat[0])
    #print(ser.ix[0])
    its = ser.__iter__()
    print(next(its))
    print(next(its))
    """""""""""


    series_1 = Series(ser.__len__)

    import time
    for i in range(0, len(ser)):
        struct_time = time.strptime(date + ' ' + ser.iloc[i], '%Y-%m-%d %X')
        timeStamp = int(time.mktime(struct_time))
        series_1[i]=timeStamp

    #print(series_1)
    return series_1


df["timestamp"]=toTimeStamp(date,ser)
"""
 # 转为时间戳
import time

struct_time = time.strptime(date +' '+ df.time, '%Y-%m-%d %X')
timeStamp = int(time.mktime(struct_time))
print(timeStamp)
df["timestamp"]=df.time

print(df)
"""
# get a list of columns
cols = list(df)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('date')))
cols.insert(0, cols.pop(cols.index('timestamp')))
cols.insert(0, cols.pop(cols.index('stocknum')))

print(cols)

df = df.ix[:, cols]
print(df)


engine = create_engine('mysql://root:root@127.0.0.1/stockdata0?charset=utf8')

#存入数据库
#df.to_sql('tick_data',engine)


#追加数据到现有表
df.to_sql('tick_data',engine,if_exists='append')

