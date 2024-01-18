from django.http import HttpResponse
from django.template import loader
from .models import Category, Product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import sample
import datetime

# Create your views here.



def login_view(request):
    categorias = Category.objects.all()
    context = {'categorias': categorias}
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
        return render(request, 'login.html', context)

    
def logout_view(request):
    logout(request)
    return redirect('page')
    

def signup_view(request):
    categorias = Category.objects.all()
    context = {'categorias': categorias}
    return render(request, 'signup.html',context)


def index_view(request):

    categorias = Category.objects.all()
    lista = []
    
    aux = []
    for i in categorias:
        aux.append(i)
    
    escolhidas = sample(aux,4)

    for i in categorias:
        categoria = Category.objects.get(pk=i.id)
        produtos_da_categoria = categoria.productcategory_set.all()
        if produtos_da_categoria:
            lista.append((categoria,produtos_da_categoria))
    
    context= {'lista': lista,
              'escolhidas': escolhidas,
              'categorias': categorias}
        
        
    
    return render(request, 'index.html', context )

def product_view(request,pk):
    categorias = Category.objects.all()
    prod = Product.objects.get(pk=pk)
    context = {"product": prod,
               'categorias': categorias }    
    return render(request,'single-product.html',context)

def dois(request,year=2000,month=1):
    html = "<h1>",year,"</h1>","<h2>",month,"</h2>"
    return HttpResponse(html)

def time_now(request):
    now = datetime.datetime.now()
    html = """<html><head><meta http-equiv="refresh" content="60"> </head><body>It is now %s.</body></html>""" % now
    return HttpResponse(html)


def order_view(request):
     # Obtém os dados do cookie "cart" ou uma lista vazia se o cookie não existir
    categorias = Category.objects.all()
    
    if request.method == 'POST':
        produto = request.POST['product_name']
        quantidade = request.POST['quantity']
        preco = request.POST['product_price']
        print(request.POST)
        preco = preco.replace(',','.')

        total = float(preco) * int(quantidade)
        
        prod_id = Product.objects.get(product_name__iexact=produto).id


        # Obtenha o carrinho da sessão ou crie um novo
        carrinho = request.session.get('cart', {})

        # Adicione o produto ao carrinho
        carrinho[prod_id] = {
        'nome': produto,
        'preco': preco,
        'quantidade':quantidade,
        'total': total,
        }

        # Atualize a sessão com o carrinho modificado
        request.session['cart'] = carrinho

    pedido = request.session.get('cart', {})
    context = {'pedido' : pedido,
               'categorias' :categorias, }
    template = loader.get_template('order.html')
    return render(request,'order.html', context)

def category_view(request, pk):

    categoria = Category.objects.get(pk=pk)
    produtos_da_categoria = categoria.productcategory_set.all()
    
    # Configurar a paginação
    paginator = Paginator(produtos_da_categoria, 1)  # 12 itens por página
    page = request.GET.get('page')

    try:
        itens_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não é um número inteiro, exibir a primeira página
        itens_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página está fora do intervalo (e.g., 9999), exibir a última página
        itens_paginados = paginator.page(paginator.num_pages)


    context = {'categoria': categoria,
               'produtos': produtos_da_categoria,
               'itens_paginados': itens_paginados}
    print(context)
    return render(request,'products.html', context)

def categories_view(request):
     categorias = Category.objects.all()
     context = {'categorias': categorias }

     return render(request, 'categorias.html',context )