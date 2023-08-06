
from tools.LogTools import Logger
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="downTickCVS3.py").getlog()

from tools import connectMySQL
cursor, db = connectMySQL.getTickCursorAndDB()#getTickCursor()

def creatTable():
    # logger.info("正在创建数据表" + "ErrorInfo")

    sqlSentence3 = "create table ErrorInfo" + "(股票代码 VARCHAR(10), 第一次出错日期 date, 连续出错次数 bigint DEFAULT 0,  名称 VARCHAR(10),\
                                   weight float,   最后更新日期 date,  primary key(股票代码) )"

    # print(sqlSentence3)
    try:
        cursor.execute(sqlSentence3)
    except Exception as msg:
        #print(str(msg))
        logger.info("数据表ErrorInfo" + "已经存在，无法再次创建");

def ErrortoDataBase(symbol, str_date, name):
    try:
        creatTable()

        import datetime
        today=datetime.date.today()
        updateSentence = "INSERT INTO ErrorInfo(股票代码, 第一次出错日期, 名称, 最后更新日期) VALUE('%s', '%s' , '%s', '%s')"%(symbol, str_date, name, today)\
                         + " ON DUPLICATE KEY UPDATE 连续出错次数=连续出错次数+1, 最后更新日期 = '%s'"%today
        print(updateSentence)
        cursor.execute(updateSentence)

        #cursor.close()
        db.commit()
        #db.close()
    except Exception as msg:
        #print(str(msg))
        logger.error(msg);

def NormaltoDataBase(symbol, name):

    try:
        creatTable()

        import datetime
        today=datetime.date.today()
        updateSentence = "INSERT INTO ErrorInfo(股票代码, 名称, 最后更新日期) VALUE('%s',  '%s', '%s')" % (symbol, name, today) \
                         + " ON DUPLICATE KEY UPDATE 连续出错次数=0"
        print(updateSentence)
        cursor.execute(updateSentence)

        # cursor.close()
        db.commit()
        # db.close()
    except Exception as msg:
        #print(str(msg))
        logger.error(msg);