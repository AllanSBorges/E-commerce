from django.contrib import admin
from django.http import HttpRequest
from .models import Product, Category, ProductCategory, Discount, Evaluation 

# Register your models here.

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductCategoryInline,
    ]

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductCategoryInline,
    ]




admin.site.register(Discount)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

# admin.site.register(ProductCategory)