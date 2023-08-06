__author__ = 'zoulida'

import datetime
import time

def dayStrToTimeStamp(dayStr = "20190521"):
    timeArray = time.strptime(dayStr, "%Y%m%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def getDayStr(days):#返回当天日期与days天之前的日期，str类型

    today = datetime.date.today()
    z30daysago = today + datetime.timedelta(days=-days)
    #startstr = '19900101'
    startstr = str(z30daysago.strftime('%Y%m%d'))
    endstr = str(today.strftime('%Y%m%d'))
    return startstr, endstr

def getDayList(startDay, endDay):#返回日期list
    return

def dateRange(beginDate, endDate):#返回日期list
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

if __name__ == '__main__':
    #print(dayStrToTimeStamp())
    print(dateRange('20160301', '20190522'))