
import tushare as ts
import pandas as pd
import pymysql
import os
import time
import urllib
import re
import traceback
import datetime

# 爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html


# 抓取网页股票代码函数
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code

def toCVS(filepath, dateend=datetime.date.today() ):
    #########################开始干活############################
    Url = 'http://quote.eastmoney.com/stocklist.html'  # 东方财富网股票数据连接地址
    #filepath = 'd:\\data\\'  # 定义数据文件保存路径
    # 实施抓取
    code = getStackCode(getHtml(Url))
    # 获取所有股票代码（以6/3/0开头的，应该是沪市数据）集合
    CodeList = []
    for item in code:
        if item[0] == '6':
            CodeList.append(item)
        if item[0] == '0':
            CodeList.append(item)
        if item[0] == '3':
            CodeList.append(item)

    import datetime
    # start = '2016-06-01'
    # end = '2017-01-01'
    #
    # datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    # dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

    datestart = dateend + datetime.timedelta(days=-30)
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        print(datestart.strftime('%Y-%m-%d'))

    OpenList = ts.trade_cal()
    print(OpenList)
    print(OpenList[2018-12-31])
def saveCVStoDoc(CodeList):
    # 抓取数据并保存到本地csv文件
    debugNum = 3
    debugBoolean = True
    for code in CodeList:

        if debugBoolean== True:#调试用
            if debugNum < 0:
                break
            debugNum -= 1

        time.sleep(2)#降低get频率
        try:
            print("start download ", code)
            df = ts.get_tick_data(code, date='2018-01-09')

            print("stock_code=" , str(code) , df.head(10))

        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            # 如果以上插入过程出错，跳过这条数据记录，继续往下进行
            continue  # break




def main():

    # 爬取程序，每天存储一个文件夹。
    filepath = 'e:\\tick_data\\'  # 定义数据文件保存路径
    import datetime
    today = datetime.date.today()
    todaystr = str(today.strftime('%Y%m%d'))
    filepath = filepath + todaystr + "\\"
    print(filepath)
    from tools import mkdir

    mkdir.mkdirA(filepath)
    toCVS(filepath)


main()