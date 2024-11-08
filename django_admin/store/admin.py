from django.contrib import admin
from .models import Category, Product, CartItem, Order, Log, TelegramUser, Newsletter

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Log)
admin.site.register(TelegramUser)
admin.site.register(Newsletter)

