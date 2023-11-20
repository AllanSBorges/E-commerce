from django.http import HttpResponse
from django.template import loader
from .models import Categories, Products
import datetime
# Create your views here.

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
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def order(request):
    template = loader.get_template('order.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())