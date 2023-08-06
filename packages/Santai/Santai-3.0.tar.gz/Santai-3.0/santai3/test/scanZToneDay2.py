__author__ = 'zoulida'

from tools.tusharePro import getPro
from tools.LogTools import Logger
import time
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="santai3").getlog()
#from tools.connectMySQL import getStockDataBaseCursorAndDB

def getProOk():#没有用到
    getPro()
def getZTList(codelist, dateDay):
    listA = []
    #if haveBeenGreaterThanbyOneDay(codelist, dateDay):
    #    listA.append(code)
def getGreaterThanList(codelist, dateDay, percentage = 1.07):#取得最高价大于percentage的list
    start = time.time()
    listA = []
    res_l = []
    pool = poolpre()
    for row in codelist.itertuples(index=True, name='Pandas'):

        code = getattr(row, "Index")
        booleanValue = pool.apply_async(haveBeenGreaterThanbyOneDay, (code, dateDay, percentage),
                         callback=None)  # apply_async(func[, args[, kwds[, callback[, error_callback]]]])
        res_l.append(booleanValue)
        # print(booleanValue.get())
        # if booleanValue.get():
        #     listA.append(code)


    print("保存中间结果~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("Sub-process(es) done.")

    stop = time.time()
    print('delay: %.3fs' % (stop - start))
    #addList(res_l)
    #print(res_l)

def addList(res_l):
    for res in res_l:
        #spend = (timest - datetime.datetime.now()).total_seconds()
        #time = datetime.datetime.now()
        #print('正在提取结果：  ', listtemp5.__len__(),'   ; 上次消耗时间 ' , spend)
        try:
            item = res.get()
        except Exception as e:
            print('traceback.print_exc():', e)
            import traceback
            traceback.print_exc()

def haveBeenGreaterThanbyOneDay(codes, dateDay ,percentage):
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
    return False

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
    return False

def getStockList():
    from tools.StockList import get_all_stock2
    codelist = get_all_stock2()
    return codelist

def poolpre():
    from multiprocessing import Pool, Manager
    from multiprocessing import cpu_count
    #print(cpu_count())
    pool = Pool(10)
    #pool = Pool(cpu_count()+2)
    return pool

percentage = 1.07
if __name__ == '__main__':
    #import datetime
    #print(datetime.datetime.today())

    codelist = getStockList()

    #code = ""
    dateDay = ""
    getGreaterThanList(codelist, dateDay)