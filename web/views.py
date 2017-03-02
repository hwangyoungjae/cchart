# -*- encoding:utf8 -*-
from django.shortcuts import render, HttpResponse, render_to_response
import random, json

# Create your views here.
def main_page(request):
    return render_to_response('main_page.html')