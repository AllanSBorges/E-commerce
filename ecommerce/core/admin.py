from django.contrib import admin
from django.http import HttpRequest
from .models import Product, Category, ProductCategory, Discount, Company 

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

class CompanyAdmin(admin.ModelAdmin):
    '''def has_add_permission(self, request):
        return False'''
    
    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(Discount)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(ProductCategory)