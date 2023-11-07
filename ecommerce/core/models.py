from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length = 30)
    product_description = models.CharField(max_length = 60)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_status = models.Boolean()
    
    
