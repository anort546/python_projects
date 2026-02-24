#1
import datetime
today=datetime.datetime.now()
new=today-datetime.timedelta(days=5)
print(new)

#2
import datetime
today=datetime.date.today()
yest=today-datetime.timedelta(days=1)
tom=today+datetime.timedelta(days=1)
print(yest)
print(tom)


#3
import datetime
now = datetime.datetime.now()
no_microsec = now.replace(microsecond=0)
print(no_microsec)


#4
import datetime
date1 = datetime.datetime(2025, 1, 31)
date2 = datetime.datetime(2026, 1, 5)
difference = date2 - date1
print(difference.total_seconds())