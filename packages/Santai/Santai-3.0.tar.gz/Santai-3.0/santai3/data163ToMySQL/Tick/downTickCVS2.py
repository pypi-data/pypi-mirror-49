import numpy as np
import pandas as pd
import tushare as ts
import datetime
import time
import tushare as ts
import os
import traceback
import logging

data_dir = 'E:\\stock_data\\tick_CVS_data\\'  # 下载数据的存放路径

# ts.get_sz50s() #获取上证50成份股  返回值为DataFrame：code股票代码 name股票名称

cal_dates = ts.trade_cal()  # 返回交易所日历，类型为DataFrame, calendarDate  isOpen


# 本地实现判断市场开市函数
#@date: str类型日期 eg.'2017-11-23'


def is_open_day(date):
    #print(cal_dates[cal_dates['calendarDate'] == date])
    if date in cal_dates['calendarDate'].values:
        return cal_dates[cal_dates['calendarDate'] == date].iat[0, 1] == 1
    return False

#dateend=datetime.date.today()
#print(is_open_day(dateend.strftime('%Y-%m-%d')))

#从TuShare获取tick data数据并保存到本地
#@symbol: str类型股票代码 eg.600030
#@date: date类型日期
def get_save_tick_data(symbol, date, name):

    #print(date,symbol)
    global sleep_time,data_dir
    sleep_time=2
    res=True
    str_date=str(date)
    dir=data_dir+str(date.year)+'\\'+str(date.month)+'\\'+symbol
    file=dir+'\\'+symbol+'_'+str_date+'_tick_data.csv'
    if is_open_day(str_date):
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(file):
            try:
                df=ts.get_tick_data(symbol,str_date,pause=0.1,src='tt')
            except IOError as msg:
                print (str(msg))#.decode('UTF-8'))
                sleep_time=min(sleep_time*2, 128)#每次下载失败后sleep_time翻倍，但是最大128s
                print ('Get tick data error: symbol: '+ symbol + ', date: '+str_date+', sleep time is: '+str(sleep_time))
                return res
            else:
                #print(df)
                df.to_csv(file)

                toMySQL(df, date, symbol, name)

                sleep_time=max(sleep_time/2, 2) #每次成功下载后sleep_time变为一半，但是至少2s
                print ("Successfully download and save file: "+file+', sleep time is: '+str(sleep_time))
                return res
        else:
            print ("Data already downloaded before, skip " + file)
            res = False
            return res



#get_save_tick_data('600030', datetime.date(2018, 7, 11))

# 获取从起始日期到截止日期中间的的所有日期，前后都是封闭区间
def get_date_list(begin_date, end_date):
    date_list = []
    while begin_date <= end_date:
        # date_str = str(begin_date)
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list


# 获取感兴趣的所有股票信息，这里只获取沪深300股票
def get_all_stock_id():
    stock_info = ts.get_hs300s()
    print(stock_info)
    return stock_info['code'].values

def get_all_stock():
    stock_info = ts.get_stock_basics()
    #print(stock_info)
    return  stock_info


def toMySQL(df, date, symbol, name):
    #print("ToDo sth")
    from tools import connectMySQL
    cursor, db = connectMySQL.getTickCursorAndDB()#getTickCursor()

    #print(df.keys())

    #创建数据表
    print("正在创建数据表" + symbol)
    sqlSentence3 = "create table tick_%s" % symbol + "(timeStamp bigint, 日期 date, 股票代码 VARCHAR(10),  名称 VARCHAR(10),\
                           tick_time time DEFAULT NULL, price float,    \
                           changeA float, volume bigint, amount bigint, type VARCHAR(10),  primary key(timeStamp))"
    try:
        cursor.execute(sqlSentence3)
    except Exception as msg:
        #print (str(msg))
        print("数据表stock_%s" % symbol + "已经存在，无法再次创建");


    for row in df.itertuples(index=True, name='Pandas'):
        #print(getattr(row, "time"), getattr(row, "volume"))
        #print(date,str(date))
        time2 = str(date) +  " " + getattr(row, "time")
        #print(time2)
        try:
            struct_time = time.strptime(time2, '%Y-%m-%d %H:%M:%S')
            tsp = int(time.mktime(struct_time))
            #print(tsp)

            sqlSentence4 = "insert IGNORE  into tick_%s" % symbol + \
                           "(timestamp, 日期, 股票代码, 名称, tick_time, price, changeA, volume, amount, type )" \
                           " values ('%s'," % tsp + "'%s',"%date + "'%s',"%symbol + "'%s',"%name + "'%s',"%getattr(row, "time") +\
                           "'%s',"%getattr(row, "price") + "'%s',"%getattr(row, "change") + "'%s',"%getattr(row, "volume") +\
                           "'%s',"%getattr(row, "amount") + "'%s'" %getattr(row, "type") +")"

            # 获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlSentence4 = sqlSentence4.replace('nan', 'null').replace('None', 'null').replace('none', 'null')

            print(sqlSentence4)
            cursor.execute(sqlSentence4)
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            # 如果以上插入过程出错，跳过这条数据记录，继续往下进行
            continue  # break

    # 关闭游标，提交，关闭数据库连接
    cursor.close()
    db.commit()
    db.close()


# 从TuShare下载感兴趣的所有股票的历史成交数据，并保存到本地HDF5压缩文件
# define the log file, file mode and logging level
logging.basicConfig(filename='TickData.log', filemode="w", level=logging.DEBUG)
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger().addHandler(console)

logging.debug('开始爬取数据。Getting tick data from Tecent.')

import datetime
today=datetime.date.today()
z30daysago = today + datetime.timedelta(days=-30)
#dates = get_date_list(datetime.date(2018, 6, 30), datetime.date(2018, 7, 16))
dates = get_date_list(z30daysago, today)
#stocks = get_all_stock_id()
stocks = get_all_stock()

#print(stocks)
for row in stocks.itertuples(index=True, name='Pandas'):
    #print(row)
    print(getattr(row, "Index"), getattr(row, "name"))
    #logging.debug("%s,%s" %(getattr(row, "Index"), getattr(row, "name")))
    for date in dates:
        print(date)
        if get_save_tick_data(getattr(row, "Index"), date, getattr(row, "name")):
            time.sleep(sleep_time)
# for stock in stocks:
#     print("stock: ",stock)
#     for date in dates:
#         #if get_save_tick_data(stock, date):
#             time.sleep(sleep_time)


