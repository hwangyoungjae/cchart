# -*- encoding:utf8 -*-
import random, json, datetime, time
import pandas_datareader.data
from django.shortcuts import render, HttpResponse, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from pandas import Series, DataFrame
from django.utils import timezone
from .models import *

# Create your views here.
def compound_data(request):
    Fluctuation_ratio = 50  # 등락비율(%)
    ratio = Fluctuation_ratio / float(100)
    init_cost = 1000000  # 백만원
    Counts = [None, ]
    Costs = ['주식가격',]
    for i in range(1,101):
        Counts.append(str(i))
        if random.choice((True, False)):
            init_cost += init_cost * ratio
            Costs.append(init_cost)
        else:
            init_cost -= init_cost * ratio
            Costs.append(init_cost)
    data = {
        'columns': [
            Counts,
            Costs,
        ]
    }
    return HttpResponse(json.dumps(data),content_type='text/json')
def compound(request):
    return render(request, 'edu/compound.html')

def costaverage_data(request):
    CODE = request.GET['code']
    SDATE_STR = request.GET['sdate']
    SDATE_DATETIME = datetime.datetime.strptime(SDATE_STR, '%Y-%m-%d')
    EDATE_STR = request.GET['edate']
    EDATE_DATETIME = datetime.datetime.strptime(EDATE_STR, '%Y-%m-%d')

    code = Code.objects.get(code=CODE)
    return_data = list()
    for stock in Stock.objects.filter(code=code, date__gte=SDATE_DATETIME, date__lte=EDATE_DATETIME).order_by('date'):
        return_data.append(
            (
                int(time.mktime(stock.date.timetuple()) * 1000),
                stock.open,
                stock.high,
                stock.low,
                stock.close,
            )
        )
    return HttpResponse(json.dumps(return_data), content_type='text/json')
def costaverage(request):
    try:
        CODE = request.GET['code']
    except KeyError:
        CODE = '035420.KS' #삼성전자

    try:
        SDATE_STR = request.GET['sdate']
        SDATE_DATETIME = datetime.datetime.strptime(SDATE_STR, '%Y-%m-%d')
    except KeyError:
        SDATE_DATETIME = datetime.datetime.now() - datetime.timedelta(days=365)
        SDATE_STR = SDATE_DATETIME.strftime('%Y-%m-%d')

    try:
        EDATE_STR = request.GET['edate']
        EDATE_DATETIME = datetime.datetime.strptime(EDATE_STR, '%Y-%m-%d')
    except KeyError:
        EDATE_DATETIME = datetime.datetime.now()
        EDATE_STR = EDATE_DATETIME.strftime('%Y-%m-%d')

    try:#DB에 있으면 PASS
        code = Code.objects.get(code=CODE)
    except ObjectDoesNotExist: #없으면 추가
        code = Code(code=CODE)
        code.save()
        DataFrame = pandas_datareader.data.DataReader(CODE, "yahoo", '1970-01-01', timezone.now())
        for index in DataFrame['Open'].index:
            Stock(code=code,
                  date=index,
                  open=DataFrame['Open'][index],
                  high=DataFrame['High'][index],
                  low=DataFrame['Low'][index],
                  close=DataFrame['Close'][index],
                  adjclose=DataFrame['Adj Close'][index],
                  volume=DataFrame['Volume'][index]
                  ).save()

    #이동평균선 구하기 위한 데이터 추출
    date_list = list()
    adjclose_list = list()
    for stock in Stock.objects.filter(code=code, date__gte=SDATE_DATETIME, date__lte=EDATE_DATETIME).order_by('date'):
        date_list.append(int(time.mktime(stock.date.timetuple()) * 1000))
        adjclose_list.append(stock.adjclose)
    series = Series(
        data=adjclose_list,
        index=date_list,
    )

    class Gen_movingaverage:
        def __init__(self,series, name, days, type='spline'):
            self.CHART = {
                'name': name,
                'id': name,
                'type': type,
                'data': list(),
            }
            self.DATA = series.rolling(window=days).mean()
            for index in self.DATA.index:
                self.CHART['data'].append((index, self.DATA[index], self.DATA[index], self.DATA[index], self.DATA[index],))
        def chart(self, tojson=True):
            if tojson:
                return json.dumps(self.CHART)
            else:
                return json.dumps(self.CHART)
        def data(self):
            return self.DATA

    M5 = Gen_movingaverage(series=series, name='M5', days=5)
    M20 = Gen_movingaverage(series=series, name='M20', days=20)


    ### Add Chart
    AddCharts = list()
    AddCharts.append(M5.chart(True))
    AddCharts.append(M20.chart(True))  # 20일 이동평균선

    ### 골든크로스
    glod_cross = {
        'type': 'flags',
        'name': 'golden cross',
        'data': list(),
        'onSeries': 'M5',
        'shape': 'squarepin',
    }
    Add = 0
    for index in M5.data().index:
        if M5.data()[index] > M20.data()[index]:
            Add += 1
        else:
            Add = 0
        print Add
        if Add == 1:
            glod_cross['data'].append({'x': index,'title': 'Golden cross'})

    ### 데드크로스
    dead_cross = {
        'type': 'flags',
        'name': 'dead cross',
        'data': list(),
        'onSeries': 'M5',
        'shape': 'squarepin',
    }
    Add = 0
    for index in M5.data().index:
        if M5.data()[index] < M20.data()[index]:
            Add += 1
        else:
            Add = 0
        print Add
        if Add == 1:
            dead_cross['data'].append({'x': index, 'title': 'Dead cross'})






    return render(request, 'edu/costaverage.html',{
        'CODE':CODE,
        'SDATE': SDATE_STR,
        'EDATE': EDATE_STR,
        'AddCharts': AddCharts,
        'GLODENCROSS':glod_cross,
        'DEADCROSS':dead_cross,
    })