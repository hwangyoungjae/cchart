# -*- encoding:utf8 -*-
import os,sys,time,datetime
import pandas_datareader.data
from pandas import Series, DataFrame
import json, math, MySQLdb

# daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
#            'high':  [12100, 11800, 11200, 11100, 11150],
#            'low' :  [11600, 11050, 10900, 10950, 10900],
#            'close': [11900, 11600, 11000, 11100, 11050]}
#
# daeshin_day = DataFrame(daeshin)
# print(daeshin_day)
#
# date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
# daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
# print daeshin_day


con = MySQLdb.connect('192.168.0.15','root','Admin2013!','cchart')
cur = con.cursor()

cur.execute('SELECT * FROM web_code;')
print cur._executed
for row in cur.fetchall():
    CODE, = row
    cur.execute('SELECT COUNT(1) FROM web_stock WHERE code_id=%s;',(CODE,))
    print cur._executed
    if not cur.fetchone()[0]:
        cur.execute('DELETE FROM web_code WHERE code=%s;',(CODE,))
        print cur._executed
con.commit()
con.close()








