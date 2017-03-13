# -*- encoding:utf8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from pandas import Series, DataFrame
from django.utils import timezone
from .models import *
import random, json, datetime, time, math, locale
import pandas_datareader.data

class sco:
    def __init__(self, func):
        self.func = func
    def __call__(self, request):
        self.request = request
        history = History(
            sco_ip=self.sco_ip(),
            sco_referer=self.sco_referer(),
            sco_current=self.sco_current(),
            sco_agent=self.sco_agent(),
            sco_method=self.sco_method(),
        )
        history.save()
        return self.func(request)
    def sco_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return self.request.META.get('REMOTE_ADDR')
    def sco_referer(self):
        try:
            return self.request.META['HTTP_REFERER']
        except KeyError:
            return ''
    def sco_current(self):
        return self.request.get_raw_uri()
    def sco_agent(self):
        return self.request.META['HTTP_USER_AGENT']
    def sco_method(self):
        return self.request.method

def dots(numeric):
    locale.setlocale(locale.LC_ALL,'')
    return locale.format('%3f',int(numeric),1).rsplit('.',1)[0]

# Create your views here.
# def compound_data(request):
#     Fluctuation_ratio = 50  # 등락비율(%)
#     ratio = Fluctuation_ratio / float(100)
#     init_cost = 1000000  # 백만원
#     Counts = [None, ]
#     Costs = ['주식가격',]
#     for i in range(1,101):
#         Counts.append(str(i))
#         if random.choice((True, False)):
#             init_cost += init_cost * ratio
#             Costs.append(init_cost)
#         else:
#             init_cost -= init_cost * ratio
#             Costs.append(init_cost)
#     data = {
#         'columns': [
#             Counts,
#             Costs,
#         ]
#     }
#     return HttpResponse(json.dumps(data),content_type='text/json')
@sco
def compound_data(request):

    cost = float(request.GET['cost'])
    change_ratio = int(request.GET['change_ratio'])
    ratio = change_ratio / float(100)
    count = int(request.GET['count'])

    data = list()
    for i in range(count):
        c = cost * ratio
        if random.choice((True, False)):
            cost += c
            cc = '+' + dots(c)
        else:
            cost -= c
            cc = '-' + dots(c)
        data.append([cost,dots(cost), cc, ])
    return HttpResponse(json.dumps(data), content_type='text/json')
@sco
def compound(request):

    try:
        change_ratio = request.GET['change_ratio'].strip()
        try:
            change_ratio = int(change_ratio)
        except ValueError:
            change_ratio = 30
        if change_ratio < 0:
            change_ratio = change_ratio - change_ratio - change_ratio
        start = True
    except KeyError:
        change_ratio = 30
        start = False

    return render(request, 'edu/compound.html',{
        'change_ratio': change_ratio,
        'start':start,
    })

@sco
def costaverage_data(request):

    CODE = request.GET['code']
    SDATE_STR = request.GET['sdate']
    SDATE_DATETIME = datetime.datetime.strptime(SDATE_STR, '%Y-%m-%d')
    EDATE_STR = request.GET['edate']
    EDATE_DATETIME = datetime.datetime.strptime(EDATE_STR, '%Y-%m-%d')

    code = Code.objects.get(code=CODE)

    # 캔들스틱 표출용
    return_data = list()
    for stock in Stock.objects.filter(code=code, date__gte=SDATE_DATETIME, date__lte=EDATE_DATETIME).order_by('date'):
        return_data.append(
            [int(time.mktime(stock.date.timetuple()) * 1000),stock.open,stock.high,stock.low,stock.close,]
        )

    #이동평균선 구하기용
    adjclose_datas = list()
    adjclose_index = list()
    for stock in Stock.objects.filter(code=code, date__gte=SDATE_DATETIME - datetime.timedelta(days=120), date__lte=EDATE_DATETIME).order_by('date'):
        adjclose_datas.append(stock.adjclose)
        adjclose_index.append(int(time.mktime(stock.date.timetuple()) * 1000))

    # 5일 이동평균선 데이터 생성
    series = Series(data=adjclose_datas, index=adjclose_index).rolling(window=5).mean()
    for index, date in enumerate([t[0] for t in return_data]):
        if math.isnan(series[date]):
            val = None
        else:
            val = series[date]
        return_data[index].append(val)

    # 20일 이동평균선 데이터 생성
    series = Series(data=adjclose_datas, index=adjclose_index).rolling(window=20).mean()
    for index, date in enumerate([t[0] for t in return_data]):
        if math.isnan(series[date]):
            val = None
        else:
            val = series[date]
        return_data[index].append(val)

    ALIST = [] # 계좌잔고
    BLIST = []  # 주식 보유 수량
    CLIST = []  # 현금 잔고
    DLIST = []  # 계좌 잔고

    BALANCE = 100000000 # 계좌 잔고(1억원)
    BUYCOST = 1000000  # 구매 금액 (백만원)
    USED_MARGIN = 0 #구매할때 사용한 금액(적립금) ,총 사용한 금액
    TRADE_COUNT = 0 #주식 보유 수량

    GOLDENCROSS = [] #골든크로스
    DEADCROSS = [] #데드크로스
    BUYPOSITION = [] #바이 포지션
    BCOUNT = 0
    SELL_FLAG = False
    START = False
    for i,item in enumerate(return_data):
        DATE, OPEN, HIGH, LOW, CLOSE, MO5, MO20 = item
        if i == 0:
            if MO5 < MO20:
                START = True
        ADSCLOSE = series[DATE]
        # print DATE,
        if MO5 > MO20:
            ''' BUY 구간 '''
            BCOUNT += 1
            SELL_FLAG = True
            if START:
                if BCOUNT == 1:
                    GOLDENCROSS.append({'x': DATE, 'title': 'GC'})
                    # print BCOUNT, 'BUY(a)',
                # else:
                #     print BCOUNT,'BUY(b)',
                # 구매 계산하기
                BUY_LOTS = int(math.floor(BUYCOST / ADSCLOSE))  # 구매 가능한 계좌수 / 버림
                REQUIRED_MARGIN = BUY_LOTS * ADSCLOSE  # 구매에 필요한 금액

                BALANCE -= REQUIRED_MARGIN
                USED_MARGIN += REQUIRED_MARGIN
                TRADE_COUNT += BUY_LOTS

                A = TRADE_COUNT * ADSCLOSE  # 그동한 구매한 주식을 판매한 금액
                B = USED_MARGIN/TRADE_COUNT #매입 평균 단가
                # print '/ 적립액:',dots(REQUIRED_MARGIN),
                # print '/ 주가:', dots(ADSCLOSE),
                # print '/ 구매좌수:', BUY_LOTS,
                # print '/ 누적좌수:', TRADE_COUNT,
                # print '/ 누적적립액:', dots(USED_MARGIN),
                # # print '/ 매입평균단가:',dots(B),
                # print '/ 판매시 잔액:',dots(BALANCE + A),
                # print
                ALIST.append((DATE, BALANCE + A))
                BLIST.append((DATE, TRADE_COUNT))
                BUYPOSITION.append({'x': DATE, 'title': 'buy'})
            else:
                # print BCOUNT, 'HOLD(c)',
                # print '/ 누적좌수:', TRADE_COUNT,
                # print '/ 잔액:',dots(BALANCE),
                # print
                ALIST.append((DATE, BALANCE))
                BLIST.append((DATE, TRADE_COUNT))
        else:
            BCOUNT = 0
            if START:
                if SELL_FLAG:
                    START = True
                    SELL_FLAG = False
                    DEADCROSS.append({'x': DATE, 'title': 'DC(SELL)'})
                    A = TRADE_COUNT * ADSCLOSE #구동한 구매한 주식을 판매한 금액

                    # print BCOUNT, 'SELL(d)',
                    # print '/ 판매액:', dots(A),
                    # print '/ 주가:', dots(ADSCLOSE),
                    # print '/ 판매좌수:', TRADE_COUNT,
                    # print '/ 누적좌수:', 0,
                    # print '/ 누적적립액:', dots(USED_MARGIN),
                    # # print '/ 매입평균단가:',dots(B),
                    # print '/ 판매시 잔액:', dots(BALANCE + A),
                    # print
                    ALIST.append((DATE, BALANCE + A))
                    BLIST.append((DATE, TRADE_COUNT))

                    BALANCE += A
                    TRADE_COUNT = 0

                else:
                    # print BCOUNT, 'HOLD(e)',
                    # print '/ 누적좌수:', TRADE_COUNT,
                    # print '/ 잔액:', dots(BALANCE),
                    # print
                    ALIST.append((DATE, BALANCE))
                    BLIST.append((DATE, TRADE_COUNT))
            else:
                if SELL_FLAG:
                    START = True
                    SELL_FLAG = False
                    DEADCROSS.append({'x': DATE, 'title': 'DC(HOLD)'})
                    # print BCOUNT, 'HOLD(f)', 'DC',
                    # print '/ 누적좌수:', TRADE_COUNT,
                    # print '/ 잔액:', dots(BALANCE),
                    # print
                    ALIST.append((DATE, BALANCE))
                    BLIST.append((DATE, TRADE_COUNT))
                else:
                    # print BCOUNT, 'HOLD(g)'
                    ALIST.append((DATE, BALANCE))
                    BLIST.append((DATE, TRADE_COUNT))

    # 계좌잔고
    A_series = Series(index=[t[0] for t in ALIST], data=[t[1] for t in ALIST])
    B_series = Series(index=[t[0] for t in BLIST], data=[t[1] for t in BLIST])
    for index, date in enumerate([t[0] for t in return_data]):
        # print index, date, series[date]
        return_data[index].append(A_series[date]) # 계좌 잔고
        if B_series[date]:
            return_data[index].append(B_series[date]) # 주식 보유 수량
        else:
            return_data[index].append(None)  # 주식 보유 수량


    return HttpResponse(json.dumps([return_data,GOLDENCROSS,DEADCROSS,BUYPOSITION,]), content_type='text/json')

@sco
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
        print Stock.objects.filter(code=code)
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

    return render(request, 'edu/costaverage.html',{
        'CODE':CODE,
        'SDATE': SDATE_STR,
        'EDATE': EDATE_STR,
        # 'GLODENCROSS':glod_cross,
        # 'DEADCROSS':dead_cross,
    })
@sco
def realtime(request):

    return render(request, 'edu/realtime.html')
@sco
def realtime_data(request):

    try:
        if request.GET['type'] == 'date':
            return HttpResponse(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),content_type='text/json')
        elif request.GET['type'] == 'init':
            datas = list()
            for i in range(-30+1, 0+1):
                data = [
                    (datetime.datetime.now() + datetime.timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S'),
                    None,
                ]
                datas.append(data)
            return HttpResponse(json.dumps(datas), content_type='text/json')
    except KeyError:
        pass


    data = [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), random.choice(range(-100,101))]
    return HttpResponse(json.dumps(data), content_type='text/json')
