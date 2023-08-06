# 导入需要使用到的模块
import urllib
import re
import pandas as pd
import pymysql
import os
import time
import traceback
import tushare as ts

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




def toCVS(filepath, isalldate=False ):
    #########################开始干活############################
    #Url = 'http://quote.eastmoney.com/stocklist.html'  # 东方财富网股票数据连接地址
    #Url = 'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'
    #filepath = 'd:\\data\\'  # 定义数据文件保存路径
    # 实施抓取
    from data163ToMySQL.Tick import downTickCVS7
    codes = downTickCVS7.get_all_stock2()#####借用函数
    # 获取所有股票代码（以6/3/0开头的，应该是沪市数据）集合
    '''CodeList = []
    for item in code:
        if item[0] == '6':
            CodeList.append(item)
        if item[0] == '0':
            CodeList.append(item)
        if item[0] == '3':
            CodeList.append(item)'''
    CodeList = []
    for row in codes.itertuples(index=True, name='Pandas'):
        CodeList.append(getattr(row, "Index"))
    # 抓取数据并保存到本地csv文件
    for code in CodeList:
        #if int(code )  >600001 or int(code )<300000:
        #    continue
        #if int(code )  > 600005 :
        #    continue
        print('正在获取股票%s数据' % code)
        import datetime
        today=datetime.date.today()
        z30daysago = today + datetime.timedelta(days=-60)
        startstr='19900101'
        if isalldate == False:
            startstr=str(z30daysago.strftime('%Y%m%d'))
        endstr = str(today.strftime('%Y%m%d'))
        #url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
        #      '&end=20181231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        #url2 = "url出错"
        #print(code[0])
        if int(code[0]) == 3 or int(code[0]) == 0:
            url2 = 'http://quotes.money.163.com/service/chddata.html?code=1' + code + '&start=' + startstr + "&end=" + endstr +\
                  '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        if int(code[0]) == 6 :
            #print("*********")
            url2 = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + '&start=' + startstr + "&end=" + endstr +\
                  '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        print(url2)
        try:
            urllib.request.urlretrieve(url2, filepath + code + '.csv')
            time.sleep(1)
        except Exception as e:
            print('traceback.print_exc():', traceback.print_exc())
            print("服务器拒绝，休息20秒")
            time.sleep(20)




# 数据库名称和密码
name = 'root'
password = 'root'  # 替换为自己的账户名和密码 

def toMySQL(formfilepath):
    ##########################将股票数据存入数据库###########################


    # 建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect('localhost', name, password, charset='utf8')
    cursor = db.cursor()
    # 创建数据库stockDataBase
    sqlSentence1 = "create database stockDataBase"
    try:
        cursor.execute(sqlSentence1)  # 选择使用当前数据库
    except:
        print("数据库已经存在，无法再次创建");
    sqlSentence2 = "use stockDataBase;"
    cursor.execute(sqlSentence2)

    # 获取本地文件列表
    fileList = os.listdir(formfilepath)
    """
    # 依次对每个数据文件进行存储
    for fileName in fileList:
        data = pd.read_csv(filepath + fileName, encoding="gbk")
        # 创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
        sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(timeStamp bigint, 日期 date, 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                           收盘价 float,    最高价    float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额    float, \
                           涨跌幅 float, 换手率 float, 成交量 bigint, 成交金额 bigint, 总市值 bigint, 流通市值 bigint, primary key(timeStamp))"
        #cursor.execute(sqlSentence3)
        #except:
        print('数据表已存在！')
    """
    for fileName in fileList:
        data = pd.read_csv(formfilepath + fileName, encoding="gbk")
        if 0 < 1:#添加table存在判断
            print("正在创建数据表" + fileName[0:6])
            sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(timeStamp bigint, 日期 date, 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                                   收盘价 float,    最高价    float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额    float, \
                                   涨跌幅 float, 换手率 float, 成交量 bigint, 成交金额 bigint, 总市值 bigint, 流通市值 bigint, primary key(timeStamp))"
            try:
                cursor.execute(sqlSentence3)  # 选择使用当前数据库
            except:
                print("数据表stock_%s" % fileName[0:6] + "已经存在，无法再次创建");

        # 迭代读取表中每行数据，依次存储（整表存储还没尝试过）
        print('正在存储stock_%s' % fileName[0:6])
        length = len(data)
        for i in range(0, length):
            record = tuple(data.loc[i])
            # print(record[0])

            # 插入数据语句
            try:

                struct_time = time.strptime(record[0], '%Y-%m-%d')
                tsp = int(time.mktime(struct_time))
                sqlSentence4 = "insert IGNORE  into stock_%s" % fileName[0:6] + "(timestamp, 日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价, 前收盘, 涨跌额, 涨跌幅, 换手率, \
                               成交量, 成交金额, 总市值, 流通市值) values ('%s'," % tsp + "'%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record

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



def queryMySQL():
    ###########################查询刚才操作的成果##################################

    # 重新建立数据库连接
    db = pymysql.connect('localhost', name, password, 'stockDataBase')
    cursor = db.cursor()
    # 查询数据库并打印内容
    cursor.execute('select * from stock_600003')
    results = cursor.fetchall()
    for row in results:
        print(row)
    # 关闭
    cursor.close()
    db.commit()
    db.close()



###################
def main():
    import logging
    # define the log file, file mode and logging level
    logging.basicConfig(filename='dayStockData.log', filemode="w", level=logging.DEBUG)
    logging.debug('开始爬取数据。Getting Stock data from 163.')

    # 爬取程序，每天存储一个文件夹。
    filepath = 'd:\\data\\'  # 定义数据文件保存路径
    import datetime
    delta = datetime.timedelta(days=0)
    today = datetime.date.today() - delta
    todaystr = str(today.strftime('%Y%m%d'))
    filepath = filepath + todaystr + "\\"
    print(filepath)
    from tools import mkdir

    mkdir.mkdirA(filepath)
    toCVS(filepath, isalldate=False)

    # 存储数据库
    toMySQL(filepath)



if __name__ == "__main__":
    main()