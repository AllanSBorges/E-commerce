from django.http import HttpResponse
from .models import Category, Product, Customer, Evaluation, Address
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import Error
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.forms import modelformset_factory
from .forms import AddressForm
from random import sample
import datetime
import requests

dados = {"loja_nome": 'Hexashop',
         "loja_cnpj": '01.304.648/0001-14',
         "loja_razao_social": 'Hexashop LTDA',
         "loja_email": 'sac@hexashop.com',
         "loja_tel": '010-020-0340',
         "loja_end": '16501 Collins Ave, Sunny Isles Beach, FL 33160, United States',
         "loja_end2": 'North Miami Beach',
         } # Dicionário alteração dos dados da loja (obs. Poderia ser uma entidade no banco de dados.)

def dados_nav(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = len(carrinho)

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod,
               'dados': dados}
    return context

# Create your views here.



def login_view(request):
    context = dados_nav(request)
    
    if ('next' in request.GET) and request.user.is_authenticated:
        proxima_pagina = request.GET['next']
        return redirect(proxima_pagina)
    
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
    return redirect('page/')
    

def signup_view(request):
    context = dados_nav(request)  

    if request.method == 'POST':
        f_name = request.POST['first-name']
        l_name = request.POST['last-name']
        u_name = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']

        logradouro = request.POST['logradouro']
        complemento = request.POST['complemento']
        cidade = request.POST['cidade']
        numero = int(request.POST['numero'])
        cep = int(request.POST['cep'])
        estado = request.POST['estado']

        usuario = Customer.objects.create_user(username=u_name, first_name = f_name, last_name = l_name, email = e, password = p)
        usuario.save()
        endereco = Address.objects.create(cep = cep, logradouro = logradouro,
                                          complemento = complemento,
                                          numero = numero,
                                          cidade = cidade,
                                          estado = estado,
                                          user_id=usuario)
        endereco.save()
        return render(request,'signup.html',context)




    return render(request, 'signup.html',context)

@login_required(login_url='/login/')
def perfil_view(request):
    context = dados_nav(request)

    if request.method == "POST":
        nome = request.POST['first-name']
        sobrenome = request.POST['last-name']
        email = request.POST['email']
      

        try:
            Customer.objects.filter(pk = request.user.id).update(first_name=nome, last_name=sobrenome, email=email)
            messages.success(request, "Perfil atualizado com sucesso.")
        except Error:
            messages.error(request, "Ops. Um erro ocorreu.")

    

    return render(request,'perfil.html', context)
    

@login_required(login_url='/login/')
def alterar_senha_view(request):
    context = dados_nav(request)

    if request.method == "POST":
        senha_atual = request.POST['senha-atual']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        
        if check_password(senha_atual,request.user.password):
            if senha1 == senha2:
                messages.success(request, "Senha alterada com sucesso.")
                request.user.set_password(senha1)
                request.user.save()
            else:
                messages.warning(request, "Nova senha e Confirmação devem ser iguais.")
        else:
            messages.error(request, "Algo de errado ocorreu. Tente novamente...")

    
        
    return render(request,'alterar.html', context)

@login_required(login_url='/login/')
def pedidos_view(request):
   context = dados_nav(request)
   
   return render(request,'pedidos.html', context)

@login_required(login_url='/login/')
def enderecos_view(request):
    context = dados_nav(request)
    

    AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=1)
    

    if request.method == 'POST':
        
        formset = AddressFormSet(request.POST, queryset=Address.objects.filter(user_id=request.user))
        
        if formset.is_valid():
            for form in formset:
                    try:
                        endereco = form.save(commit=False)
                        endereco.user_id = request.user
                        endereco.save()
                    except Error:
                        pass
                    
            return redirect('enderecos/')
    else:
        formset = AddressFormSet(queryset=Address.objects.filter(user_id=request.user))
    
    context.setdefault('formset',formset)


    return render(request, 'enderecos.html', context)

@login_required(login_url='/login/')
def entrega_view(request):
    context = dados_nav(request)
    enderecos = Address.objects.filter(user_id=request.user)
    if not enderecos:
        messages.warning(request, "Por favor cadastre pelo menos um endereço para a entrega.")

    total = request.session.get('total', 0 )

    if total != 0:
        pass

    if request.method == "POST":
        escolhido = request.POST.get('escolhido')
        print(escolhido)
        context.setdefault('escolhido', escolhido)
    else:
        escolhido = ""    
    


    context.setdefault('enderecos', enderecos)
    

    return render(request, 'entrega.html', context)


def index_view(request):
    context = dados_nav(request)

    categorias = Category.objects.all()
    lista = []
    
    aux = []
    for i in categorias:
        aux.append(i)
    
    if aux:
        if len(aux) < 4:
            num = len(aux)
        else:
            num = 4
        escolhidas = sample(aux,num) 
    else:
        escolhidas = []

    for i in categorias:
        categoria = Category.objects.get(pk=i.id)
        produtos_da_categoria = categoria.productcategory_set.all()
        if produtos_da_categoria:
            lista.append((categoria,produtos_da_categoria))
    
    context.setdefault('lista', lista)
    context.setdefault('escolhidas', escolhidas)
              
        
        
    
    return render(request, 'index.html', context )

def product_view(request,pk):
    context = dados_nav(request)

    prod = Product.objects.get(pk=pk)
    context.setdefault('product', prod)
                   
    return render(request,'single-product.html',context)

def dois(request,year=2000,month=1):
    html = "<h1>",year,"</h1>","<h2>",month,"</h2>"
    return HttpResponse(html)

def time_now(request):
    now = datetime.datetime.now()
    html = """<html><head><meta http-equiv="refresh" content="60"> </head><body>It is now %s.</body></html>""" % now
    return HttpResponse(html)


def order_view(request):

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

    request.session['total'] = total
    context = dados_nav(request)

    
    context.setdefault('pedido', pedido)
    context.setdefault('total', total)
               
    
    
    return render(request,'order.html', context)


@login_required(login_url='/login/')
def confirmar_view(request):
    context = dados_nav(request)    

    if request.method == "POST":
        
        i = 0
        for key, value in request.POST.items():
            print(key, value)
        while True:
            quantidade = "quantity"+str(i)
            
            if request.POST.get(quantidade):
                print(request.POST.get(quantidade))
            else:
                break
            i += 1
        
  

    
    return render(request,'confirmar.html', context)

def category_view(request, pk):
    context = dados_nav(request)
    

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


    context.setdefault('categoria', categoria)
    context.setdefault('produtos', produtos_da_categoria)
    context.setdefault('itens_paginados', itens_paginados)
               
    
    return render(request,'products.html', context)

def categories_view(request):
     context = dados_nav(request)

     return render(request, 'categorias.html',context )

@login_required(login_url='/login/')
def avaliar_view(request, pk):
    context = dados_nav(request)
    product = Product.objects.get(pk=pk)

    context.setdefault('product', product)
                
    
    user_id = int(request.user.id)
    cliente = Customer.objects.get(pk=user_id)
    obj = Evaluation.objects.get(product_id = product, customer_id = cliente )
    if obj:
        context.setdefault('nota', obj.nota)
        context.setdefault('avaliacao', obj.avaliacao)
    else:
        context.setdefault('nota', 5)
        context.setdefault('avaliacao', '')


    if request.method == "POST":
        nota = int(request.POST['nota'])
        avaliacao = request.POST['avaliacao']
        

        product_id = Product.objects.get(pk=pk)
        user_id = int(request.user.id)
        cliente = Customer.objects.get(pk=user_id)
        
        
        try:
            Evaluation.objects.update_or_create(customer_id = cliente, product_id = product_id,                                                 
                                                defaults = {'customer_id':cliente,
                                                            'product_id': product_id,
                                                            'avaliacao': avaliacao,
                                                            'nota': nota})            
            messages.success(request, "Agradecemos sua por sua avaliação.")

        except Error:
            messages.error(request, "Ops. Algo deu errado.\nTente realizar sua avaliação novamente.\n")
        
                                          
    return render(request, 'avaliar.html',context )

def visualizar_view(request, pk):
    context = dados_nav(request)
    product = Product.objects.get(pk=pk)
    context.setdefault('product', product)                
    return render(request, 'visualizar.html',context )