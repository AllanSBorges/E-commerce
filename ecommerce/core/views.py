from django.http import HttpResponse
from django.template import loader
from .models import Category, Product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


import datetime
# Create your views here.



def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		# Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('login')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

    
def logout_view(request):
    logout(request)
    return redirect('index')
    

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def page(request):
    template = loader.get_template('index.html')
    context = {"nome": "Allan",
               "data_nasc": "22/07/1991", }    
    return HttpResponse(template.render(context))

def product(request):
    template = loader.get_template('single-product.html')
    context = {"nome": "Allan",
               "data_nasc": "22/07/1991", }    
    return HttpResponse(template.render(context))

def dois(request,year=2000,month=1):
    html = "<h1>",year,"</h1>","<h2>",month,"</h2>"
    return HttpResponse(html)

def time_now(request):
    now = datetime.datetime.now()
    html = """<html><head><meta http-equiv="refresh" content="60"> </head><body>It is now %s.</body></html>""" % now
    return HttpResponse(html)


def order(request):
    template = loader.get_template('order.html')
    return HttpResponse(template.render())

