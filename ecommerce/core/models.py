from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length = 30)
    product_description = models.CharField(max_length = 60)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_status = models.BooleanField()

class Categories(models.Model):
    category_name = models.CharField(max_length = 30)
    category_description = models.CharField(max_length = 60)
    
class ProductCategories(models.Model):
    product_id = models.ForeignKey("Products", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Categories", on_delete=models.CASCADE)
    

    
    
    
