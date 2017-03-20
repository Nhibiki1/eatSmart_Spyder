import datetime
import time


def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

print(Caltime( '2017-03-20 10:36:37', '2017-03-27 10:38:52').total_seconds())
print(Caltime( '2017-03-20 10:36:37', '2017-03-27 10:38:52') > 7)
