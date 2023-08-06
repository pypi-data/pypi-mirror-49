import pymysql


# 数据库名称和密码
name = 'root'
password = 'root'  # 替换为自己的账户名和密码
mysqlNodeIP = '202.194.246.167'


def getTickCursorAndDB():

    # 建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect('localhost', name, password, charset='utf8')
    cursor = db.cursor()
    # 创建数据库stockDataBase
    sqlSentence1 = "create database TickData"
    try:
        cursor.execute(sqlSentence1)  # 选择使用当前数据库
    except:
        print("数据库已经存在，无法再次创建");
    sqlSentence2 = "use TickData;"
    cursor.execute(sqlSentence2)
    return cursor,db

def getStockDataBaseCursorAndDB():

    # 建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect(mysqlNodeIP, name, password, charset='utf8')
    cursor = db.cursor()
    #print(db, cursor)
    # 创建数据库stockDataBase
    sqlSentence1 = "create database stockDataBase"
    try:
        cursor.execute(sqlSentence1)  # 选择使用当前数据库
    except:
        print("数据库已经存在，无法再次创建");
    sqlSentence2 = "use stockDataBase;"
    cursor.execute(sqlSentence2)
    return cursor,db

def getEngine():
    from sqlalchemy import create_engine
    engine = create_engine('mysql://%s:%s@127.0.0.1/stockDataBase?charset=utf8' % (name, password))
    return engine