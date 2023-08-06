__author__ = 'zoulida'
# -*- coding=utf-8 -*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
# 每天的涨跌停
import re
import time
import xlrd
import xlwt
import sys
import os
#import setting
#from setting import is_holiday, DATA_PATH
import pandas as pd
import tushare as ts
#from setting import llogger
import requests
#from send_mail import sender_139
import datetime
# reload(sys)
# sys.setdefaultencoding('gbk')

from tools.LogTools import *
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="santai3").getlog()


class GetZDT:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        #self.today = datetime.date(2018, 7, 11)
        self.today = time.strftime("%Y%m%d")
        self.today = '20190520'
        DIR_DATA_PATH = "d:\zdtDATA"
        #self.path = DATA_PATH
        self.zdt_url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/' + \
            self.today + ".js"
        #"http://homeflashdata2.jrj.com.cn/limitStatistic/ztForce/20190520.js"
        self.zrzt_url = 'http://hqdata.jrj.com.cn/zrztjrbx/limitup.js' #昨日涨停

        self.host = "home.flashdata2.jrj.com.cn"
        self.reference = "http://stock.jrj.com.cn/tzzs/zdtwdj/dtforce.shtml"

        self.header_zdt = {"User-Agent": self.user_agent,
                           "Host": self.host,
                           "Referer": self.reference}

        self.zdt_indexx = [u'代码', u'名称', u'最新价格', u'涨跌幅', u'封成比', u'封流比', u'封单金额', u'最后一次涨停时间', u'第一次涨停时间', u'打开次数',
                           u'振幅',
                           u'涨停强度']

        self.zrzt_indexx = [u'序号', u'代码', u'名称', u'昨日涨停时间', u'最新价格', u'今日涨幅', u'最大涨幅', u'最大跌幅', u'是否连板', u'连续涨停次数',
                            u'昨日涨停强度', u'今日涨停强度', u'是否停牌', u'昨天的日期', u'昨日涨停价', u'今日开盘价格', u'今日开盘涨幅']
        self.header_zrzt = {"User-Agent": self.user_agent,
                            "Host": "hqdata.jrj.com.cn",
                            "Referer": "http://stock.jrj.com.cn/tzzs/zrztjrbx.shtml"
                            }
        self.DIR_DATA_PATH = "d:\zdtDATA"
        if not os.path.exists(DIR_DATA_PATH):
            os.mkdir(DIR_DATA_PATH)

    #@staticmethod
    def getdata(self, url, headers, retry=2):
        for i in range(retry):
            try:
                resp = requests.get(url=url, headers=headers)
                resp.encoding = 'gbk' #UnicodeEncodeError: 'gbk' codec can't encode character '\ufffd'
                if resp.status_code == 200:

                    content = resp.text
                # md_check = re.findall('summary|lasttradedate|month|market', content) #这种判断方式是查关键词，比较繁琐落后。
                # if content and len(md_check) > 0:
                    return content
                else:
                    time.sleep(0)
                    logger.info('failed to get content, retry: {}'.format(i))
                    continue
            except Exception as e:
                logger.info(e)
                time.sleep(0)
                continue
        return None

    def convert_json(self, content):
        p = re.compile(r'"Data":(.*)};', re.S)
        if len(content) <= 0:
            logger.info('Content\'s length is 0')
            exit(0)
        result = p.findall(content)
        if result:
            try:
                # print(result)
                t1 = result[0]
                t2 = list(eval(t1))
                return t2
            except Exception as e:
                logger.info(e)
                return None
        else:
            return None

    # 2016-12-27 to do this
    def save_excel(self, date, data):
        # data is list type
        w = xlwt.Workbook(encoding='gbk')
        ws = w.add_sheet(date)
        excel_filename = date + ".xls"
        # sheet=open_workbook(excel_filenme)
        # table=wb.sheets()[0]
        xf = 0
        ctype = 1
        rows = len(data)
        point_x = 1
        point_y = 0
        ws.write(0, 0, u'代码')
        ws.write(0, 1, u'名称')
        ws.write(0, 2, u'最新价格')
        ws.write(0, 3, u'涨跌幅')
        ws.write(0, 4, u'封成比')
        ws.write(0, 5, u'封流比')
        ws.write(0, 6, u'封单金额')
        ws.write(0, 7, u'第一次涨停时间')
        ws.write(0, 8, u'最后一次涨停时间')
        ws.write(0, 9, u'打开次数')
        ws.write(0, 10, u'振幅')
        ws.write(0, 11, u'涨停强度')
        print("Rows:%d" % rows)
        for row in data:
            rows = len(data)
            cols = len(row)
            point_y = 0
            for col in row:
                # print(col)
                # table.put_cell(row,col,)
                # print(col)
                ws.write(point_x, point_y, col)
                # print("[%d,%d]" % (point_x, point_y))
                point_y = point_y + 1

            point_x = point_x + 1

        w.save(excel_filename)

    def save_to_dataframe(self, data, indexx, choice, post_fix):
        #engine = setting.get_engine('db_zdt')
        if not data:
            exit()
        data_len = len(data)
        if choice == 1:
            for i in range(data_len):
                data[i][choice] = data[i][choice]

        df = pd.DataFrame(data, columns=indexx)

        filename = os.path.join(
            self.path, self.today + "_" + post_fix + ".xls")

        # 今日涨停
        if choice == 1:
            df['今天的日期'] = self.today
            df.to_excel(filename, encoding='gbk')
            try:
                #df.to_sql(self.today + post_fix, engine, if_exists='fail')
                print(df)
            except Exception as e:
                logger.info(e)
        # 昨日涨停
        if choice == 2:
            df = df.set_index(u'序号')
            df[u'最大涨幅'] = df[u'最大涨幅'].map(lambda x: round(x * 100, 3))
            df[u'最大跌幅'] = df[u'最大跌幅'].map(lambda x: round(x * 100, 3))
            df[u'今日开盘涨幅'] = df[u'今日开盘涨幅'].map(lambda x: round(x * 100, 3))
            df[u'昨日涨停强度'] = df[u'昨日涨停强度'].map(lambda x: round(x, 0))
            df[u'今日涨停强度'] = df[u'今日涨停强度'].map(lambda x: round(x, 0))
            try:
                #df.to_sql(self.today + post_fix, engine, if_exists='fail')
                df.to_excel('testzrt.xls', encoding='gbk')
                print(df)
            except Exception as e:
                logger.info(e)

            avg = round(df['今日涨幅'].mean(), 2)
            current = datetime.datetime.now().strftime('%Y-%m-%d')
            title = '昨天涨停个股今天{}\n的平均涨幅{}\n'.format(current, avg)
            try:
                #sender_139(title, title)
                print(title)
            except Exception as e:
                print(e)

    # 昨日涨停今日的状态，今日涨停


    def zhangtingStockProcess(self, dayStr):#首先判断数据库是否有，如果有什么都不做；没有则写入csv以及利用pd。tosql存入数据库。

        timeArray = time.strptime(dayStr, "%Y%m%d")
        timeStamp = int(time.mktime(timeArray))
        #判断是否已经下载了
        try:
            import tools.connectMySQL as cm
            engine = cm.getEngine()
            cnx = engine.raw_connection()
            data = pd.read_sql('SELECT * FROM zhangting where 时间戳 = %s' % timeStamp, cnx)
            if(data.__len__() > 0):
                return
                #print(data.__len__())

        except Exception as e:
            #print('traceback.print_exc():', traceback.print_exc())
            logger.info(e)


        zdt_url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/' + \
                       dayStr + ".js"
        print(zdt_url)

        # 涨停
        zdt_content = self.getdata(zdt_url, headers=self.header_zdt)
        if zdt_content is None:
            return
        logger.info('zdt Content' + zdt_content)
        zdt_js = self.convert_json(zdt_content)

        #保存CSV
        data = zdt_js
        indexx = self.zdt_indexx
        if not data:
            return

        df = pd.DataFrame(data, columns=indexx)
        path = self.DIR_DATA_PATH + "\zhangting"
        filename = os.path.join(
            path, dayStr + "_" + 'zhangting' + ".csv")

        if not os.path.exists(path):
            os.mkdir(path)

        df['日期'] = dayStr

        df['时间戳'] = timeStamp
        df.to_csv(filename, encoding='gbk')


        #保存数据库
        try:
            import tools.connectMySQL as cm
            engine = cm.getEngine()
            df.to_sql('zhangting', engine, if_exists='append', index=False)

        except Exception as e:
            logger.info(e)

        #time.sleep(0.5)

    def dietingStockProcess(self, dayStr):#首先判断数据库是否有，如果有什么都不做；没有则写入csv以及利用pd。tosql存入数据库。

        timeArray = time.strptime(dayStr, "%Y%m%d")
        timeStamp = int(time.mktime(timeArray))
        #判断是否已经下载了
        try:
            import tools.connectMySQL as cm
            engine = cm.getEngine()
            cnx = engine.raw_connection()
            data = pd.read_sql('SELECT * FROM dieting where 时间戳 = %s' % timeStamp, cnx)
            if(data.__len__() > 0):
                return
                #print(data.__len__())

        except Exception as e:
            #print('traceback.print_exc():', traceback.print_exc())
            logger.info(e)


        zdt_url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/dtForce/' + \
                       dayStr + ".js"
        print(zdt_url)

        # 涨停
        zdt_content = self.getdata(zdt_url, headers=self.header_zdt)
        if zdt_content is None:
            return
        logger.info('zdt Content' + zdt_content)
        zdt_js = self.convert_json(zdt_content)

        #保存CSV
        data = zdt_js
        indexx = self.zdt_indexx
        if not data:
            return

        df = pd.DataFrame(data, columns=indexx)
        path = self.DIR_DATA_PATH + "\dieting"
        filename = os.path.join(
            path, dayStr + "_" + 'dieting' + ".csv")

        if not os.path.exists(path):
            os.mkdir(path)

        df['日期'] = dayStr

        df['时间戳'] = timeStamp
        df.to_csv(filename, encoding='gbk')


        #保存数据库
        try:
            import tools.connectMySQL as cm
            engine = cm.getEngine()
            df.to_sql('dieting', engine, if_exists='append', index=False)

        except Exception as e:
            logger.info(e)

        #time.sleep(0.5)

    def zdtStockAllDays(self):#只执行一次，并否每天执行
        from tools.timeTools import dateRange
        dayslist = dateRange('20190301', '20190522')
        for oneday in dayslist:
            #self.zhangtingStockProcess(oneday)
            self.dietingStockProcess(oneday)
            time.sleep(0.5)
            print('oneday is ' + oneday)

    strtest = 'var min={"time":"2019-05-27 15:18:48","Data":[[925,6,6,["预盈预增","新股","基金重仓股","抗抑郁"}'


    def storedata(self):
        self.zdtStockAllDays()

        # 涨跌停1分钟数据统计
        zdt1fzsjtj = 'http://homeflashdata2.jrj.com.cn/limitStatistic/min_and_concept.js'
        #zdt1fzsjtj_content = self.getdata(zdt1fzsjtj, headers=self.header_zdt)
        #logger.info('zdt1fzsjtj Content' + zdt1fzsjtj_content)
        # p = re.compile(r'{[\w\W]*}', )
        # if len(self.strtest) <= 0:
        #     logger.info('Content\'s length is 0')
        #     exit(0)
        # result = p.findall(self.strtest)
        # print(result)
        #print(self.convert_json(self.strtest))
'''
        #昨日涨停表现
        zrzt_content = self.getdata(self.zrzt_url, headers=self.header_zrzt)
        logger.info('zrzt Content' + zdt_content)
        zrzt_js = self.convert_json(zrzt_content)
        self.save_to_dataframe(zrzt_js, self.zrzt_indexx, 2, 'zrzt')
        time.sleep(0.5)

        #跌停
        self.dt_url = 'http://home.flashdata2.jrj.com.cn/limitStatistic/dtForce/20190520.js'
        dt_content = self.getdata(self.dt_url, headers=self.header_zdt)
        logger.info('dt Content' + dt_content)

        #涨跌停历史数据
        zdtlssj = 'http://homeflashdata2.jrj.com.cn/limitStatistic/month/201905.js'
        zdtlssj_content = self.getdata(zdtlssj, headers=self.header_zdt)
        logger.info('zdtlssj Content' + zdtlssj_content)

        #市场温度
        scwd = 'http://homeflashdata2.jrj.com.cn/limitStatistic/market.js'
        scwd_content = self.getdata(scwd, headers=self.header_zdt)
        logger.info('scwd Content' + scwd_content)

        #涨跌停1分钟数据统计
        zdt1fzsjtj = 'http://homeflashdata2.jrj.com.cn/limitStatistic/min_and_concept.js'
        zdt1fzsjtj_content = self.getdata(zdt1fzsjtj, headers=self.header_zdt)
        logger.info('zdt1fzsjtj Content' + zdt1fzsjtj_content)
'''

if __name__ == '__main__':
    # today='2018-04-16'
    # 填补以前的数据
    # x=pd.date_range('20170101','20180312')
    # date_list = [datetime.datetime.strftime(i,'%Y%m%d') for i in list(pd.date_range('20170401','20171231'))

    # if is_holiday():
    #     logger.info('Holiday')
    #     exit()
    logger.info("start")
    obj = GetZDT()
    obj.storedata()