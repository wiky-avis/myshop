from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # добавляет возможность изменять 
    # перечисленные поля со страницы списка товаров, не переходя к форме 
    # редактирования товара
    prepopulated_fields = {'slug': ('name',)} # мы настраиваем поле slug так, 
    # чтобы его значение формировалось автоматически из поля name

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)