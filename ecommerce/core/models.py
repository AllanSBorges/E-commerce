from django.db import models
from django.contrib.auth.models import User, AbstractUser



# Create your models here.

class Customer(AbstractUser):
    
    
    def __str__(self):
        return self.username

class Product(models.Model):
    product_name = models.CharField(max_length = 30)
    product_description = models.CharField(max_length = 60)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_status = models.BooleanField()
    product_image = models.ImageField(null=True)

class Category(models.Model):
    category_name = models.CharField(max_length = 30)
    category_description = models.CharField(max_length = 60)
    
class ProductCategory(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)
    

class Order(models.Model):
    order_client = models.ForeignKey("Customer", on_delete=models.CASCADE)
    order_status = models.CharField(max_length = 15)
    order_date = models.DateField(auto_now=True)
    order_total = models.DecimalField(max_digits=7, decimal_places=2)

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
    user_id = models.ForeignKey("Customer", on_delete=models.CASCADE)


    
    
