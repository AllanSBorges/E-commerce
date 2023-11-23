from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class CustomUser(User):
    # Adicione campos adicionais, se necessário
    pass


class Products(models.Model):
    product_name = models.CharField(max_length = 30)
    product_description = models.CharField(max_length = 60)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_status = models.BooleanField()
    product_image = models.ImageField(null=True)

class Categories(models.Model):
    category_name = models.CharField(max_length = 30)
    category_description = models.CharField(max_length = 60)
    
class ProductCategories(models.Model):
    product_id = models.ForeignKey("Products", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Categories", on_delete=models.CASCADE)
    

class Orders(models.Model):
    order_status = models.CharField(max_length = 15)
    order_date = models.DateField(auto_now=True)
    order_total = models.DecimalField(max_digits=7, decimal_places=2)

class OrderProducts(models.Model):
    item_id = models.ForeignKey("Products", on_delete=models.CASCADE)
    order_id = models.ForeignKey("Orders", on_delete=models.CASCADE)
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    item_quantity = models.PositiveIntegerField()
    
class Address(models.Model):
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE)


    
    
