from django.http import HttpResponse
from .models import Category, Product, Customer, Evaluation, Address, Order, OrderProduct, Discount, DiscountOrder
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
         "loja_tel": '(22) 38534334',
         "loja_end":  'Rua Projetada',
         "loja_cep": '33160',
         "loja_end_num": '16501',
         "loja_end_bairo": "Sunny Isles Beach",
         "loja_end_estado": "FL",
         "loja_end_pais": "United States",
         "escritorio_email": 'sac@hexashop.com',
         "escritorio_tel": '010-020-0340',
         "escritorio_end":  'Collins Ave, ,  33160, ',
         "escritorio_end_num": '16501',
         "escritorio_end_bairo": "Sunny Isles Beach",
         "escritorio_end_estado": "FL",
         "escritorio_end_pais": "United States",

        } # Dicionário alteração dos dados da loja (obs. Poderia ser uma entidade no banco de dados.)

def dados_nav(request):
    categorias = Category.objects.all()
    carrinho = request.session.get('cart', {})
    qtd_prod = 0
    if len(carrinho):
        for item in carrinho.values():
            qtd_prod += int(item['quantidade'])
    
        

    aux = []
    for i in categorias:
        aux.append(i)
    
    if aux:
        if len(aux) < 5:
            num = len(aux)
        else:
            num = 5
        rodape = sample(aux,num) 
    else:
        rodape = []

    context = {'categorias': categorias,
               'qtd_prod': qtd_prod,
               'dados': dados,
               'rodape': rodape }
    return context

def media_avaliacao(request,product_id):
    produto = Product.objects.get(pk = product_id)
    avaliacoes = Evaluation.objects.filter(produto_id = produto)
    media = 0
    if avaliacoes:
        for avaliacao in avaliacoes:
            media += avaliacao.nota
        media = int(media/len(avaliacoes))
        return media
    else:
        return 5

# Create your views here.


def pagina_nao_encontrada(request, exception=None):
    return render(request, '404.html', status=404)

def login_view(request):
    context = dados_nav(request)
    tentativas = int(request.session.get('tentativas', 0))
    
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
            tentativas = 0 
            request.session['tentativas'] = tentativas
            messages.success(request, "Login realizado com sucesso!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            tentativas += 1
            request.session['tentativas'] = tentativas
            messages.error(request, "Login ou senha inválidos, Por favor tente novamente...")
            return redirect('login/')
    else:
        context.setdefault('tentativas',tentativas)
        return render(request, 'login.html', context)

    
def logout_view(request):
    request.session['tentativas'] = 0
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

        try:
            usuario = Customer.objects.create_user(username=u_name, first_name = f_name, last_name = l_name, email = e, password = p)
            usuario.save()
        except Error:
            messages.error(request, "Ops. Nome de Usuário já cadastrado.")
            return render(request,'signup.html',context)
        

        try:
            endereco = Address.objects.create(cep = cep, logradouro = logradouro,
                                          complemento = complemento,
                                          numero = numero,
                                          cidade = cidade,
                                          estado = estado,
                                          user_id=usuario)
            endereco.save()
        except Error:
            messages.error(request, "Ops. Error ao cadastrar seu endereço.")
        
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

   user_id = int(request.user.id)
   cliente = Customer.objects.get(pk = user_id)
   pedidos = Order.objects.filter(order_client = cliente)

   # Configurar a paginação
   if pedidos:
       paginator = Paginator(pedidos, 10)  # 10 itens por página
       page = request.GET.get('page')
       try:
           itens_paginados = paginator.page(page)
       except PageNotAnInteger:
           # Se a página não é um número inteiro, exibir a primeira página
           itens_paginados = paginator.page(1)
       except EmptyPage:
           # Se a página está fora do intervalo (e.g., 9999), exibir a última página
           itens_paginados = paginator.page(paginator.num_pages)
        
       context.setdefault('itens_paginados',itens_paginados)
   return render(request,'pedidos.html', context)

@login_required(login_url='/login/')
def pedido_view(request,pk):
    context = dados_nav(request)
    pedido = Order.objects.get(pk=pk)
    items = OrderProduct.objects.filter(order_id = pedido)
    
    dados_pedido = {}
    for index,item in enumerate(items):
        preco = item.item_price
        quantidade = item.item_quantity
        nome = item.item_id.product_name

        dados_pedido.setdefault(index, {'nome': nome,
                                        'preco': preco,
                                        'quantidade': quantidade})
    print(dados_pedido)

        

    return render(request, 'pedido.html', context)

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
    if context['qtd_prod'] == 0:
        return redirect('/')

    


    if not enderecos:
        messages.warning(request, "Por favor cadastre pelo menos um endereço para a entrega.")

    total = request.session.get('total', 0 )

    if total != 0:
        pass

   


    if request.method == "POST":
        


        escolhido = request.POST.get('escolhido')
        print(escolhido)
        context.setdefault('escolhido', escolhido)
        total_weight = 0
        total_height = 0
        total_width = 0
        total_length = 0

        

       
        if escolhido != None:
            
            messages.warning(request, """Seria utilizado algum serviço de Entrega de terceiros para realizar o calculo do frete, previsão de entrega, rastreio do pedido, o que no momento vai além do objetivo deste projeto.""")

            carrinho = request.session.get('cart')
            print(carrinho)
            if carrinho:
                for v in carrinho.values():
                    produto = Product.objects.get(product_name=v['nome'])
                    total_height += produto.product_height * int(v['quantidade'])
                    total_weight += produto.product_weight * int(v['quantidade'])
                    total_width += produto.product_width * int(v['quantidade'])
                    total_length += produto.product_length * int(v['quantidade'])

                
                url = 'https://api.melhorenvio.com.br/v2/calculator'
                headers = {'Authorization': 'Token SEU_TOKEN_AQUI'}
                payload = {'from': dados['loja_cep'], 'to': escolhido, 'weight': str(total_weight), 'height': str(total_height), 'width': str(total_width), 'length': str(total_length)}

                # response = requests.post(url, headers=headers, data=payload)
                # resultado = response.json()


                valor_frete = 35
                valor_com_frete = total + valor_frete
                context.setdefault('total',total)
                context.setdefault('valor_frete',valor_frete)
                context.setdefault('valor_com_frete',valor_com_frete)
                request.session['total'] = total
                request.session['valor_frete'] = valor_frete
                request.session['valor_com_frete'] = valor_com_frete

    else:
        escolhido = ""    
    


    context.setdefault('enderecos', enderecos)
    

    return render(request, 'entrega.html', context)

@login_required(login_url='/login/')
def pagamento_view(request):
    context = dados_nav(request)
    if request.method == "POST":
        print("Teste")
    return render(request, 'confirmar.html', context)


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
def forma_pagamento_view(request):
    context = dados_nav(request)

    if context['qtd_prod'] == 0:
        return redirect('/')    


    valor_com_frete = round(float(request.session.get('valor_com_frete',0)),2)
           
    if request.method == "POST":
        messages.warning(request, """Seria utilizado algum serviço de Pagamento de terceiros válidar a transação,
                          o que no momento vai além do objetivo deste projeto.""")
        codigo_promocional =  request.POST['CodigoPromocional']
        context.setdefault('avancar',True)

        
        desconto = Discount.objects.filter(codigo=codigo_promocional)
        if len(desconto):
            if desconto[0].validade.date() >= datetime.date.today():
                percentagem_desc = desconto[0].porcentagem / 100
                percentagem_vlw = round(valor_com_frete * percentagem_desc,2)
                valor_final = round(valor_com_frete - percentagem_vlw,2)
                context.setdefault('desconto', percentagem_vlw)            
                context.setdefault('valor_final', valor_final )
                context.setdefault('total', valor_com_frete )
                request.session['desconto'] = desconto[0].codigo
                
        else:
            context.setdefault('total',valor_com_frete )
            context.setdefault('valor_final',valor_com_frete)
            if 'desconto' in context: context.pop('desconto')
            if 'desconto' in request.session: request.session.pop('desconto')
            

        
        pagamento = request.POST['forma_pagamento']
        context.setdefault('escolhido',pagamento)
        match pagamento:

            case "Boleto":
                context['valor_final'] = round(float(context.get('valor_final',0)) * 0.95, 2)
                request.session['forma'] = 'boleto'

            case "Cartão de Crédito":
                context['valor_final'] = round(float(context.get('valor_final',0)) * 0.95, 2)
                request.session['forma'] = 'cartao'                

            case "PIX":
                request.session['forma'] = 'pix'

            case _:
                if 'forma' in request.session: request.session.pop('forma')

        

    else:
        context.setdefault('avancar',False)
        context.setdefault('total',valor_com_frete )
        context.setdefault('valor_final',valor_com_frete)

    request.session['valor_final'] = context.get('valor_final')
    return render(request,'forma_pagamento.html', context)

@login_required(login_url='/login/')
def conclusao_view(request):
    context = dados_nav(request)

    if context['qtd_prod'] == 0:
        return redirect('/')
    
    print(request.session.items())

    
    forma = request.session.get('forma')
    valor_final = request.session.get('valor_final')
    pedido = Order(order_client = request.user, order_status = "Pagamento Pendente", order_total = valor_final, order_payment_method = forma)
    cart_items = request.session['cart']
    pedido.save()

    for item in cart_items:
        product = Product.objects.filter( product_name = cart_items[item]['nome'])[0]
        item_price = round(float(cart_items[item]['preco']),2)
        item_quantidade = int(cart_items[item]['quantidade'])
        orderProd = OrderProduct(item_id = product, order_id = pedido, item_price = item_price, item_quantity = item_quantidade)
        orderProd.save()
    #print(request.session.items())


    return render(request, 'conclusao.html',context)

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

     # Configurar a paginação
    
    categorias = Category.objects.all()
    print(categorias)
    paginator = Paginator(categorias,4)  # 12 itens por página
    page = request.GET.get('page')

    try:
        itens_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não é um número inteiro, exibir a primeira página
        itens_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página está fora do intervalo (e.g., 9999), exibir a última página
        itens_paginados = paginator.page(paginator.num_pages)
    print(itens_paginados)

    context.setdefault('itens_paginados', itens_paginados)

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