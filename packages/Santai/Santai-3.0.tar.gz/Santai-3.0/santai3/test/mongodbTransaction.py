__author__ = 'zoulida'
import pymongo


user = "root"              # 数据库用户名
password = "root"       # 数据库密码
db_name = "your_db"           # 库名称
mechanism = "SCRAM-SHA-1"      # 加密方式，注意，不同版本的数据库加密方式不同。


"""mongodb配置信息"""
mongodb_setting = {
    "host": "localhost:27017",   # 数据库服务器地址
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
        return cls.instance

def get_client() -> pymongo.MongoClient:
    """
    获取一个MongoClient(一般用于生成客户端session执行事物操作)
    :return:
    """
    mongo_client = DB()
    return mongo_client

"""开始测试事务,注意: t1和t2请提前创建,事务不会自己创建collection"""
client = get_client()
t1 = client[db_name]['t1']  # 操作t1表的collection,db_name是你的数据库名,你可以这么写client.db_name.collection_name
t2 = client[db_name]['t2']  # # 操作t2表的collection
with client.start_session(causal_consistency=True) as session:
    """事物必须在session下执行,with保证了session的正常关闭"""
    with session.start_transaction():
        """一旦出现异常会自动调用session.abort_transaction()"""
        t1.insert_one(document={"name": "jack"}, session=session)  # 注意多了session这个参数
        k = dict()['name']  # 制造一个错误,你会发现t1和t2的插入都不会成功.
        t2.insert_one(document={"name": "jack2"}, session=session)