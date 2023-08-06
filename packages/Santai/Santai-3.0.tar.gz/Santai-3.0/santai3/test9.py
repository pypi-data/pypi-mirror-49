import tushare as ts

df=ts.get_hist_data('600848')
print(df)

df = ts.get_tick_data('600848',date='2017-06-19',src='tt')
print(df.head(10))

#df2 = ts.get_today_all()
#print(df2)

#df = ts.get_realtime_quotes('000581') #Single stock symbol
#df[['code','name','price','bid','ask','volume','amount','time']]



