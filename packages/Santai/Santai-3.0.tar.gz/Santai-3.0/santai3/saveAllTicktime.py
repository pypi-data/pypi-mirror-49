import defToMySQL as dtm

obj=dtm.SaveToMySQL()
obj.stockNumAndDate()

import datetime
begin = datetime.date(2018,6,1)
end = datetime.date(2018,7,7)
d = begin
delta = datetime.timedelta(days=1)
while d <= end:
    print (d.strftime("%Y-%m-%d"))
    #print(d)
    d += delta