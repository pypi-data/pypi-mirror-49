import time

struct_time = time.strptime("30 Nov 00", "%d %b %y")
#print("%y-%m-%d" %struct_time)
#print ("returned tuple: %s " %struct_time)

print(time.strptime('2018-07-01 23:21:09', '%Y-%m-%d %X'))

print(time.strptime('2018-07-01 ', '%Y-%m-%d '))

date1='2018-07-05'

time1='09:25:13'

struct_time = time.strptime("30 Nov 00", "%d %b %y")
struct_time = time.strptime('2018-07-01 ', '%Y-%m-%d ')

struct_time = time.strptime(date1 +' '+ time1, '%Y-%m-%d %X')

 # 转为时间戳
timeStamp = int(time.mktime(struct_time))
print (timeStamp)