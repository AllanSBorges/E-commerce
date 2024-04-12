from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.


class Customer(AbstractUser):
   
    
    class Meta:
        verbose_name= 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name','last_name']
    
    def __str__(self):
        return self.first_name

class Subscriber(models.Model):
    subscriber_name = models.CharField(max_length = 30, verbose_name='Inscrito')
    subscriber_email = models.EmailField()

    class Meta:
        verbose_name = 'Inscrito'
        verbose_name_plural = 'Inscritos'
        ordering = ['subscriber_name']
    
    def __str__(self):
        return self.subscriber_name
    
class Product(models.Model):
    product_name = models.CharField(max_length = 30, verbose_name='Produto')
    product_description = models.CharField(max_length = 60, verbose_name='Descrição')
    product_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Preço')
    product_status = models.BooleanField(verbose_name='Disponível')
    product_image = models.ImageField(null=True, verbose_name='Imagem')

    
    product_netweight = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Peso líquido (em Kg):")
    product_weight = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Peso bruto (em Kg):")
    product_height = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Altura (em cm):")
    product_width = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Largura (em cm):")
    product_length = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Profundidade (em cm):")


    class Meta:
        verbose_name= 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['product_name']
    
    def __str__(self):
        return self.product_name


class Category(models.Model):
    category_name = models.CharField(max_length = 30, verbose_name='Categoria')
    category_description = models.CharField(max_length = 60, verbose_name='Descrição')
    category_breve = models.CharField(max_length = 45, blank=True, null=True, verbose_name='Descrição breve')
    category_image = models.ImageField(null=True, verbose_name='Imagem')

    class Meta:
        verbose_name= 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['category_name']
    
    def __str__(self):
        return self.category_name
    
class ProductCategory(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category_id} - {self.product_id}"

    class Meta:
        verbose_name= 'Categoria'
        verbose_name_plural = 'Categorias'
    

class Order(models.Model):
    order_client = models.ForeignKey("Customer", on_delete=models.CASCADE)
    order_status = models.CharField(max_length = 15)
    order_date = models.DateField(auto_now=True)
    order_total = models.DecimalField(max_digits=7, decimal_places=2)
    order_payment_method = models.CharField(max_length = 15)

class OrderProduct(models.Model):
    item_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    item_quantity = models.PositiveIntegerField()
    
class Address(models.Model):
    cep = models.IntegerField()
    logradouro = models.CharField(max_length = 30)
    complemento = models.CharField(max_length = 30, blank=True, null=True)
    numero = models.IntegerField()
    cidade = models.CharField(max_length = 30)
    estado = models.CharField(max_length = 30)
    user_id = models.ForeignKey("Customer", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.logradouro}, {self.complemento}, {self.numero}, {self.cidade}, {self.cep},  {self.estado}"

class Evaluation(models.Model):
    customer_id = models.ForeignKey("Customer", on_delete=models.CASCADE)
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    avaliacao = models.CharField(max_length = 30, blank=True, null=True, verbose_name = "Avaliação")
    nota = models.IntegerField()

    class Meta:
        # restrição única para evitar avaliações duplicadas pelo mesmo usuário para o mesmo produto
        unique_together = ('customer_id', 'product_id') # Pode deixar descontinuada no futuro


class Discount(models.Model):
    descricao = models.CharField(max_length = 30)
    validade = models.DateTimeField(auto_now=False, auto_now_add=False)
    porcentagem = models.PositiveIntegerField()
    codigo = models.CharField(max_length = 15)

    class Meta:
        verbose_name = 'Desconto'
        verbose_name_plural = 'Descontos'

class DiscountOrder(models.Model):
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    discount_id = models.ForeignKey("Discount", on_delete=models.CASCADE)
    discount_value = models.DecimalField(max_digits=7, decimal_places=2)