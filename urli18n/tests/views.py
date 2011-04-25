# -*- coding: utf-8 -*-

from django import http

def view1(request):
    return http.HttpResponse()

def view2(request):
    return http.HttpResponse()

def view3(request, year, month):
    return http.HttpResponse('%s-%s' % (year, month))

def view4(request, year, month, day):
    return http.HttpResponse('%s-%s-%s' % (year, month, day))
