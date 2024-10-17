from datetime import datetime, timedelta, date, time

time1 = time(0,0,0)
time2 = time(4,0,0)
time3 = time(8,0,0)
time4 = time(12,0,0)
time5 = time(16,0,0)
time6 = time(20,0,0)
time7 = time(23,59,0)

timepair_list = [(time1,time2),
(time2,time3),
(time3,time4),
(time4,time5),
(time5,time6),
(time6,time7)]

date = date(2024,10,16)

for item1,item2 in timepair_list:
	print(datetime.combine(date,item1),datetime.combine(date,item2))


datetime1 = datetime.combine(date,time1)
#print (datetime1)