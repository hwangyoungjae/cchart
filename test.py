# -*- encoding:utf8 -*-
import os,sys,time,MySQLdb
from pandas import Series
def cursor2dict(cursor,values,wrap_func=None):
    if values:
        fieldnames=[t[0] for t in cursor.description]
        if type(values[0]) == tuple:#fetchall
            RESULT=list()
            for row in values:
                returnItem=dict()
                for i in range(len(fieldnames)):
                    if wrap_func:returnItem[fieldnames[i]]=wrap_func(row[i])
                    else:returnItem[fieldnames[i]]=row[i]
                RESULT.append(returnItem)
        else:#fetchone
            RESULT=dict()
            for i in range(len(fieldnames)):
                if wrap_func:RESULT[fieldnames[i]]=wrap_func(values[i])
                else:RESULT[fieldnames[i]]=values[i]
        return RESULT
    else:
        return values

con = MySQLdb.connect('10.32.8.181', 'cchart', 'cchart', 'cchart')
cur = con.cursor()
cur.execute('SELECT * FROM web_stock WHERE code_id=%s;',('035420.KS',))
data = cursor2dict(cur,cur.fetchall())

moving_average_line_series = Series(
        data=[t['adjclose'] for t in data],
        index=[t['date'] for t in data],)
