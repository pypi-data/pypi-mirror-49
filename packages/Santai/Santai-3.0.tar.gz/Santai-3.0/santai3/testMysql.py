__author__ = 'Administrator'

from tools.LogTools import Logger
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="downTickCVS3.py").getlog()

from tools import connectMySQL
cursor, db = connectMySQL.getTickCursorAndDB()#getTickCursor()

#print(df.keys())

#创建数据表
logger.info("正在创建数据表" + "ErrorInfo")

sqlSentence3 = "create table ErrorInfo" + "(股票代码 VARCHAR(10), 第一次出错日期 date, 连续出错次数 bigint DEFAULT 0,  名称 VARCHAR(10),\
                           weight float,  primary key(股票代码) )"

print(sqlSentence3)
try:
    cursor.execute(sqlSentence3)
except Exception as msg:
    #print (str(msg))
    logger.info("数据表ErrorInfo"  + "已经存在，无法再次创建");



updateSentence ="INSERT INTO ErrorInfo(股票代码, 第一次出错日期, 名称, weight) VALUE('100001','2017-7-24' ,'小李','666') ON DUPLICATE KEY UPDATE 名称= '小张',weight=weight+1"
cursor.execute(updateSentence)
print(updateSentence)
cursor.close()
db.commit()
db.close()