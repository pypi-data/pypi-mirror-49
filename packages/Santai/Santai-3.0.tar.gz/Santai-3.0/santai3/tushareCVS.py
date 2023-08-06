import tushare as ts
from tools import mkdir

mkdir.mkdirA("d:/day")

df = ts.get_hist_data('300022')
#直接保存
df.to_csv('d:/day/300022.csv')

#print(ts.get_k_data('600000'))

print(ts.get_k_data('300022', ktype='5'))

#选择保存
#df.to_csv('d:/day/000875.csv',columns=['open','high','low','close'])






