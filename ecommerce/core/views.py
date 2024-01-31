from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, Customer, Avaliacao
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import Error
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from random import sample
import datetime

# Create your views here.



def login_view(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod}
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
		# Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "Login ou senha inválidos, Por favor tente novamente...")
            return redirect('login')
    else:
        return render(request, 'login.html', context)

    
def logout_view(request):
    logout(request)
    return redirect('page')
    

def signup_view(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)


    context = {'categorias': categorias,
               'qtd_prod': qtd_prod }

    if request.method == 'POST':
        f_name = request.POST['first-name']
        l_name = request.POST['last-name']
        u_name = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']

        logradouro = request.POST['logradouro']
        complemento = request.POST['complemento']
        cidade = request.POST['cidade']
        numero = request.POST['numero']
        cep = request.POST['cep']

        usuario = Customer.objects.create_user(username=u_name, first_name = f_name, last_name = l_name, email = e, password = p)
        usuario.save()
        return render(request,'signup.html',context)




    return render(request, 'signup.html',context)

@login_required(login_url='/login/')
def perfil_view(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    if request.method == "POST":
        nome = request.POST['first-name']
        sobrenome = request.POST['last-name']
        email = request.POST['email']
      

        try:
            Customer.objects.filter(pk = request.user.id).update(first_name=nome, last_name=sobrenome, email=email)
            messages.success(request, "Perfil atualizado com sucesso.")
        except Error:
            messages.error(request, "Ops. Um erro ocorreu.")

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod}

    return render(request,'perfil.html', context)
    

@login_required(login_url='/login/')
def alterar_senha(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    if request.method == "POST":
        senha_atual = request.POST['senha_atual']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        
        if check_password(senha_atual,request.user.password):
            if senha1 == senha2:
                messages.success(request, "Senha alterada com sucesso.")
                request.user.set_password(senha1)
            else:
                messages.warning(request, "Senha 1 e senha 2 não são iguais.")
        else:
            messages.error(request, "Algo de errado ocorreu.</br>Tente novamente...")

    context = {'categorias': categorias,               
               'qtd_prod': qtd_prod}
        
    return render(request,'alterar.html', context)

@login_required(login_url='/login/')
def pedidos_view(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    context = {'categorias': categorias,               
               'qtd_prod': qtd_prod}


    return render(request,'pedidos.html', context)

@login_required(login_url='/login/')
def enderecos_view(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    context = {'categorias': categorias,               
               'qtd_prod': qtd_prod}

    return render(request, 'enderecos.html', context)



         


        





    
    

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod}
    
    return render(request, 'alterar.html', context)

def index_view(request):
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

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
              'categorias': categorias,
              'qtd_prod': qtd_prod}
        
        
    
    return render(request, 'index.html', context )

def product_view(request,pk):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    prod = Product.objects.get(pk=pk)
    context = {'product': prod,
               'categorias': categorias,
               'qtd_prod': qtd_prod }    
    return render(request,'single-product.html',context)

def dois(request,year=2000,month=1):
    html = "<h1>",year,"</h1>","<h2>",month,"</h2>"
    return HttpResponse(html)

def time_now(request):
    now = datetime.datetime.now()
    html = """<html><head><meta http-equiv="refresh" content="60"> </head><body>It is now %s.</body></html>""" % now
    return HttpResponse(html)


def order_view(request):
   
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    
    
    if request.method == 'POST':
        produto = request.POST['product_name']
        quantidade = request.POST['quantity']
        preco = request.POST['product_price']
        preco = preco.replace(',','.')

        subtotal = round(float(preco) * int(quantidade),2)
        
        prod_id = Product.objects.get(product_name__iexact=produto).id


        # Obtenha o carrinho da sessão ou crie um novo
        carrinho = request.session.get('cart', {})

        # Adicione o produto ao carrinho
        
        carrinho[str(prod_id)] = {
        'nome': produto,
        'preco': preco,
        'quantidade':quantidade,
        'subtotal': subtotal,
        }

        if int(quantidade) == 0:
            carrinho.pop(str(prod_id))       


        # Atualize a sessão com o carrinho modificado
        request.session['cart'] = carrinho

    # Obtém os dados do cookie "cart" ou uma lista vazia se o cookie não existir
    pedido = request.session.get('cart', {})
    total = 0
    
    for prod in pedido.keys():
        total += float(pedido[prod]['subtotal'])

    qtd_prod = len(carrinho)
    context = {'pedido' : pedido,
               'categorias' :categorias,
               'total': total,
               'qtd_prod': qtd_prod }
    
    
    return render(request,'order.html', context)


@login_required(login_url='/login/')
def confirmar_view(request):
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)
    categorias = Category.objects.all()

    

    if request.method == "POST":
        
        i = 0
        for key, value in request.POST.items():
            print(key, value)
        while True:
            quantidade = "quantity"+str(i)
            print('aa')
            if request.POST.get(quantidade):
                print(request.POST.get(quantidade))
            else:
                break
            i += 1
        
  

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod }
    return render(request,'confirmar.html', context)

def category_view(request, pk):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    categoria = Category.objects.get(pk=pk)
    produtos_da_categoria = categoria.productcategory_set.all()
    
    # Configurar a paginação
    paginator = Paginator(produtos_da_categoria, 12)  # 12 itens por página
    page = request.GET.get('page')

    try:
        itens_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não é um número inteiro, exibir a primeira página
        itens_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página está fora do intervalo (e.g., 9999), exibir a última página
        itens_paginados = paginator.page(paginator.num_pages)


    context = {'categorias': categorias,
               'categoria': categoria,
               'produtos': produtos_da_categoria,
               'itens_paginados': itens_paginados,
               'qtd_prod': qtd_prod}
    print(context)
    return render(request,'products.html', context)

def categories_view(request):
     categorias = Category.objects.all()
     carrinho = request.session.get('cart', {})
     qtd_prod = len(carrinho)

     context = {'categorias': categorias,
                'qtd_prod': qtd_prod }

     return render(request, 'categorias.html',context )

@login_required(login_url='/login/')
def avaliar_view(request, pk):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)
    product = Product.objects.get(pk=pk)

    context = {'categorias': categorias,
                'qtd_prod': qtd_prod,
                'product': product }
    
    if request.method == "POST":
        nota = int(request.POST['nota'])
        avaliacao = request.POST['avaliacao']
        print(nota,avaliacao, sep=':')
        print(request.POST)

        product_id = Product.objects.get(pk=pk)
        user_id = int(request.user.id)
        cliente = Customer.objects.get(pk=user_id)
        
        try:
            obj = Avaliacao.objects.create(customer_id = cliente, product_id = product_id ,avaliacao = avaliacao, nota = nota)
            obj.save()
            messages.success(request, "Agradecemos sua por sua avaliação.")

        except Error:
            messages.error(request, "Ops. Algo deu errado.\nTente realizar sua avaliação novamente.\n")
                                          
    return render(request, 'avaliar.html',context )

def visualizar_view(request, pk):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)
    product = Product.objects.get(pk=pk)

    context = {'categorias': categorias,
                'qtd_prod': qtd_prod,
                'product': product }

    return render(request, 'visualizar.html',context )

