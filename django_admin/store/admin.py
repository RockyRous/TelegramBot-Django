from django.contrib import admin
from .models import Category, Product, CartItem, Order, Log

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Log)
