from django.http import HttpResponse
# Create your views here.

def page(request):
    html = "<h1>Hello World</h1>"
    return HttpResponse(html)

def dois(request):
    html = "<h1>2</h1>"
    return HttpResponse(html)