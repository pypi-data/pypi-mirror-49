__author__ = 'zoulida'

def getPro():
    import tushare as ts
    pro = ts.pro_api('69d6b836725cd75df21b39873603b14fed58d101bc033b991b51eb41')
    return pro