__author__ = 'zoulida'

import shelve,time

d = shelve.open('shelve_test')  # 打开一个文件

print("----------写----------")

info ={"name":'lilei',"sex":"man"}
name = ["autuman", "zhangsan", "lisi"]

d["teacher"] = name
d["student"] = info
d["date"] = time.ctime()

print("--------读------------")
print(d.get("teacher"))
print(d.get("student"))
print(d.get("date"))
