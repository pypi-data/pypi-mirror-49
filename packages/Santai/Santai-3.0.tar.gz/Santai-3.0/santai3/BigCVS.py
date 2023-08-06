import tushare as ts
import os
from tools import mkdir

mkdir.mkdirA("d:/HS300Days")
list = ts.get_hs300s()
#print(list)
filename = 'd:/day/bigfile.csv'
for index, row in list.iterrows():
    #print(index)
    code = row['code']
    print(code)
    filename = 'd:/HS300Days/%s.csv' %code
    df = ts.get_hist_data(code)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None)
    else:
        df.to_csv(filename)