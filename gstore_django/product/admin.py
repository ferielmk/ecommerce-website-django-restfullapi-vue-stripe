from django.contrib import admin

# Register your models here.
from .models import Category, Product, Brand, Wish, Sale

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Wish)
admin.site.register(Sale)