__author__ = 'zoulida'

import tushare as ts
from tools.LogTools import Logger
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="downTickCVS3.py").getlog()
codeset = [
    '000001.SH',
    '000300.SH',
    '000905.SH',
    '399001.SZ',
    '399005.SZ',
    '399006.SZ',
    '399016.SZ',
    '399300.SZ',

]
#描述：目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
#邹立达算法：获得数据库最大日期，再从这个日期做为开始日期下载指数。
'''
    ts_code  trade_date  turnover_rate     pe
0  000001.SH   20181018           0.38  11.92
1  000300.SH   20181018           0.27  11.17
2  000905.SH   20181018           0.82  18.03
3  399001.SZ   20181018           0.88  17.48
4  399005.SZ   20181018           0.85  21.43
5  399006.SZ   20181018           1.50  29.56
6  399016.SZ   20181018           1.06  18.86
7  399300.SZ   20181018           0.27  11.17
'''

pro = ts.pro_api('69d6b836725cd75df21b39873603b14fed58d101bc033b991b51eb41')

def saveIndex_Daily(code):
    import tools.connectMySQL as CL
    cursor, db = CL.getStockDataBaseCursorAndDB()
    start_date = None
    try:
        sqlSentence = "SELECT max(trade_date) FROM stockdatabase.stock_index_daily where ts_code = '%s'" % code
        #cursor.execute('select * from %s where 日期 between \'%s\'' % (code , startdate) + ' and \'%s\'' % enddate)
        cursor.execute(sqlSentence)

        results = cursor.fetchone()
        #df = pd.DataFrame(list(results))
        timestr = str(results[0])
        #print(str(results[0]))

        import datetime#, timedelta
        start_dateForm = datetime.datetime.strptime(timestr, "%Y%m%d")
        start_dateForm = start_dateForm + datetime.timedelta(days=1)
        start_date = start_dateForm.strftime("%Y%m%d")
        print('指数下载开始日期：', start_date)
    except Exception as msg:
        #print(str(msg))
        logger.error(msg)
    finally:
        # 关闭游标，提交，关闭数据库连接
        cursor.close()
        db.commit()
        db.close()


    df = pro.index_daily(ts_code=code, start_date = start_date, end_date = None)

    print(df)

    #from sqlalchemy import create_engine
    #engine = create_engine('mysql://root:root@127.0.0.1/stockDataBase?charset=utf8')
    from tools.connectMySQL import getEngine
    engine = getEngine()

    #存入数据库
    df.to_sql('stock_index_daily', engine, if_exists='append')

def download_indexSets(codesetS = codeset):
    for code in codesetS:
        saveIndex_Daily(code)

if __name__ == "__main__":
    download_indexSets(codesetS = codeset)