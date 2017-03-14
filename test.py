# -*- encoding:utf8 -*-
import os,sys,time,datetime
import pandas_datareader.data
from pandas import Series, DataFrame
import pandas
import json, math, MySQLdb, random


from pandas import Series, DataFrame
a = Series(list())
for date,data in [['2015-01-01',123],['2015-01-02',132],['2015-01-03',321],]:




# cnt = 100
#
# daeshin = {
#     'open':  [random.choice(range(10000,15000)) for t in range(cnt)],
#     'high':  [random.choice(range(10000,15000)) for t in range(cnt)],
#     'low' :  [random.choice(range(10000,15000)) for t in range(cnt)],
#     'close': [random.choice(range(10000,15000)) for t in range(cnt)],
# }
#
# index = pandas.date_range('20160101',periods=len(daeshin['open']))
#
#
# daeshin_day = DataFrame(data=daeshin,index=index)
# import matplotlib.pyplot as plt
# daeshin_day.plot()
# plt.show()



# print(daeshin_day)
#
# date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
# daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
# print daeshin_day


# con = MySQLdb.connect('192.168.0.15','root','Admin2013!','cchart')
# cur = con.cursor()
#
# cur.execute('SELECT * FROM web_code;')
# print cur._executed
# for row in cur.fetchall():
#     CODE, = row
#     cur.execute('SELECT COUNT(1) FROM web_stock WHERE code_id=%s;',(CODE,))
#     print cur._executed
#     if not cur.fetchone()[0]:
#         cur.execute('DELETE FROM web_code WHERE code=%s;',(CODE,))
#         print cur._executed
# con.commit()
# con.close()








