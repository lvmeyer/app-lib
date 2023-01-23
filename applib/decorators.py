from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, resolve_url


def seller_required(function):
    def wrapper(request, *args, **kw):
        user=request.user  
        if not (user.id and user.role == 2):
            return HttpResponseRedirect('/')
        else:
            return function(request, *args, **kw)
    return wrapper