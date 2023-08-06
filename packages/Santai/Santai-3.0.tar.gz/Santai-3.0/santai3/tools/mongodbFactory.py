__author__ = 'zoulida'

from pymongo import MongoClient

conn = MongoClient('202.194.246.155', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建

def getClient():
    return conn

def getConnectionWuDuJi():
    return db.WuDuJi

def dropCollection(dataset):
    #dataset = db.dataset1
    dataset.drop()

if __name__ == '__main__':
    dropCollection(getConnectionWuDuJi())

'''
user = "your_account"              # 数据库用户名
password = "your_password"       # 数据库密码
db_name = "your_db"           # 库名称
mechanism = "SCRAM-SHA-1"      # 加密方式，注意，不同版本的数据库加密方式不同。


"""mongodb配置信息"""
mongodb_setting = {
    "host": "server_ip:27017",   # 数据库服务器地址 
    "localThresholdMS": 30,  # 本地超时的阈值,默认是15ms,服务器超过此时间没有返回响应将会被排除在可用服务器范围之外
    "maxPoolSize": 100,  # 最大连接池,默认100,不能设置为0,连接池用尽后,新的请求将被阻塞处于等待状态.
    "minPoolSize": 0,  # 最小连接池,默认是0.
    "waitQueueTimeoutMS": 30000,  # 连接池用尽后,等待空闲数据库连接的超时时间,单位毫秒. 不能太小.
    "authSource": db_name,  # 验证数据库
    'authMechanism': mechanism,  # 加密
    "readPreference": "primaryPreferred",  # 读偏好,优先从盘,如果是从盘优先, 那就是读写分离模式
    "username": user,       # 用户名
    "password": password    # 密码
}


class DB:
    """自定义单例模式客户端连接池"""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            conns = pymongo.MongoClient(**mongodb_setting)
            cls.instance = conns
            return cls.instance'''
