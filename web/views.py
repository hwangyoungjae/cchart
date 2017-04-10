# -*- encoding:utf8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import random, json, uuid
import numpy as np
from .models import *

# Create your views here.
class View_csrf_exempt(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

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

@sco
def main_page(request):
    try:
        graph = request.GET['graph'].lower()
    except KeyError:
        graph = 'sin'
    
    if graph == 'sigmoid':
        chart1data = list()
        for x in np.arange(-10,10,0.5):
            y = 1 / (1 + np.exp(-1 * x))
            chart1data.append([x,y])
        chart = dict()
        chart['title'] = {'text':'sigmoid'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': '1/(1+exp(-1*x))','data': chart1data})
    elif graph == 'relu':
        chart1data = list()
        step = 0.01
        for x in np.arange(-20,20 + step, step):
            y = max([0,x])
            chart1data.append([x,y])
        chart = dict()
        
        chart['title'] = {'text':'ReLU'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'max(0,x)','data': chart1data})
    elif graph == 'leakyrelu':
        chart1data = list()
        step = 1
        for x in np.arange(-20,20 + step, step):
            y = max([0.01*x,x])
            chart1data.append([x,y])
        chart = dict()
        chart['title'] = {'text':'Leaky ReLU'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'max(0,x)','data': chart1data})
    elif graph == 'test':
        chart1data = list()
        step = 0.01
        for x in np.arange(0,6.29, step):
            chart1data.append([np.sin(x),np.cos(x)])
        chart = dict()
        chart['title'] = {'text':'test'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'max(0,x)','data': chart1data})
        
    elif graph == 'exp':
        chart1data = list()
        step = 0.01
        for x in np.arange(-10,10+step, step):
            chart1data.append([x,np.exp(x)])
        chart = dict()
        chart['title'] = {'text':'Exponentiation'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'max(0,x)','data': chart1data})
    
    elif graph == 'log':
        chart1data = list()
        step = 0.01
        for x in np.arange(0.1,5+step, step):
            chart1data.append([x,np.log(x)])
        chart = dict()
        chart['title'] = {'text':'Logarithm'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'max(0,x)','data': chart1data})
        
    else:
        chart1data = list()
        chart2data = list()
        for x in np.arange(-100,100,1.0):
            y = np.sin(3*x)
            chart1data.append([x,y])
        for x in np.arange(-100,100,1.0):
            y = np.sin(x)
            chart2data.append([x,y])
        chart = dict()
        chart['title'] = {'text':'sin'}
        chart['chart'] = {'type':'line'}
        chart['xAxis'] = {'title':{'text':'x'}}
        chart['yAxis'] = {'title':{'text':'y'}}
        chart['series'] = list()
        chart['series'].append({'name': 'sin(3x)','data': chart1data})
        chart['series'].append({'name': 'sin(x)','data': chart2data})
    
    output = request.META['REMOTE_ADDR'] + '|' + request.META['HTTP_USER_AGENT']
    response = render(request,'main_page.html',{
        'output':output,
        'chart':json.dumps(chart),
        })
    return response











