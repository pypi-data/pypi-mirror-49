__author__ = 'zoulida'
import tushare as ts
import pandas as pd

data=ts.get_hist_data('000001')
print(data)