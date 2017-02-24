# -*- encoding:utf8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
import random, json

# Create your views here.
def data_json(request):
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

def main_page(request):
    return render_to_response('main_page.html')