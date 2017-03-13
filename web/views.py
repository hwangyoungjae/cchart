# -*- encoding:utf8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import random, json, uuid
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
    response = render(request,'main_page.html')
    return response

@sco
def request_page(request):
    data = list()
    for key in dir(request):
        data.append((key,getattr(request,key)))
    return render(request, 'request_page.html', {'data':data})
@sco
def request_meta_page(request):
    data = list()
    for k,v in request.META.items():
        data.append((k,v))
    return render(request, 'request_page.html', {'data': data})
@sco
def test_page(request):
    return HttpResponse('test_page')

class test(View_csrf_exempt):
    def get(self, request):
        return HttpResponse(str(request.method))
    def post(self, request):
        return self.get(request)
