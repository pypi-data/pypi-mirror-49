import pandas as pd

data = {'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Chongqing'],
        'year': [2016, 2016, 2015, 2017, 2016, 2016],
        'population': [2100, 2300, 1000, 700, 500, 500]}
frame = pd.DataFrame(data, columns=['year', 'city', 'population', 'debt'])

# 使用apply函数, 如果city字段包含'ing'关键词，则'判断'这一列赋值为1,否则为0
frame['panduan'] = frame.city.apply(lambda x: 1 if 'ing' in x else 0)
frame['add'] = frame.population +1
frame['bbb'] = frame["population"] +2
print(frame)

# get a list of columns
cols = list(frame)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('bbb')))
print(cols)

frame = frame.ix[:, cols]
print(frame)