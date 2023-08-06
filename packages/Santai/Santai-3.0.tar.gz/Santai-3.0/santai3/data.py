import tushare as ts

# print(ts.get_hist_data('600848'))
# print(ts.cap_tops())

# print(ts.inst_tops())

# print(ts.broker_tops())
# print(ts.get_hist_data('600848', ktype='5'))



df = ts.get_today_ticks('002312')
print(df)