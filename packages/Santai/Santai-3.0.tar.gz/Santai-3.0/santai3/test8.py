__author__ = 'Administrator'

symbol = 'kk'
tsp = 'kdkd'
record = ""

sqlSentence4 = "insert IGNORE  into tick_%s" % symbol + \
                           "(timestamp, 日期, 股票代码, 名称, tick_time, price, changeA, volume, amount, type, )" \
                           " values ('%s'," % tsp + "'%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record

# 获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
sqlSentence4 = sqlSentence4.replace('nan', 'null').replace('None', 'null').replace('none', 'null')

print(sqlSentence4)