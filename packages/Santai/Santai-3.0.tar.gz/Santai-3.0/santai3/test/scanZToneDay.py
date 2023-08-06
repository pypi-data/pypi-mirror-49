__author__ = 'zoulida'

from tools.tusharePro import getPro
from tools.LogTools import Logger
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="santai3").getlog()
#from tools.connectMySQL import getStockDataBaseCursorAndDB

def getProOk():#没有用到
    getPro()
def getZTList(codelist, dateDay):
    listA = []
    #if haveBeenGreaterThanbyOneDay(codelist, dateDay):
    #    listA.append(code)
def getGreaterThanList(codelist, dateDay, percentage = 1.07):#取得最高价大于percentage的list
    listA = []
    for row in codelist.itertuples(index=True, name='Pandas'):
        code = getattr(row, "Index")
        if haveBeenGreaterThanbyOneDay(code, dateDay, percentage):
            listA.append(code)
    print(listA)

def haveBeenGreaterThanbyOneDay(code, dateDay ,percentage):
    import tools.connectMySQL as CL
    cursor, db = CL.getStockDataBaseCursorAndDB()
    #start_date = None
    try:
        sqlSentence = "SELECT * FROM stockdatabase.stock_%s where 日期 =  \'%s\' and 最高价 > %s * 前收盘 "  % (code, '2017-09-04', percentage)
        print(sqlSentence)

        cursor.execute(sqlSentence)

        results = cursor.fetchone()
        print(results)
        if results is not None:
            return True

    except Exception as msg:
        #print(str(msg))
        logger.error(msg)
    finally:
        # 关闭游标，提交，关闭数据库连接
        cursor.close()
        db.commit()
        db.close()


def getStockList():
    from tools.StockList import get_all_stock2
    codelist = get_all_stock2()
    return codelist

def poolpre():
    from multiprocessing import Pool, Manager
    from multiprocessing import cpu_count
    #print(cpu_count())
    pool = Pool(cpu_count()+2)
    return pool

percentage = 1.07
if __name__ == '__main__':
    #import datetime
    #print(datetime.datetime.today())

    codelist = getStockList()

    #code = ""
    dateDay = ""
    getGreaterThanList(codelist, dateDay)