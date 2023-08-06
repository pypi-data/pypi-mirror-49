__author__ = 'zoulida'
import tushare as ts

df1 = ts.get_realtime_quotes('000581') #Single stock symbol
#df[['code','name','price','bid','ask','volume','amount','time']]
#print(df1)

df = ts.get_today_ticks()

print(df)