from django.db import models
from django.contrib.auth.models import User

""" 
    User
Управление учетными записями пользователей.
Аутентификация и авторизация пользователей.
Хранение основной информации, такой как имя пользователя, пароль и email.
"""

class Category(models.Model):
    """ Категории
    Модель Category используется для создания иерархии категорий товаров.
    Она может иметь родительскую категорию, что позволяет создавать подкатегории.
    """
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Продукт """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    """
    Модель CartItem используется для хранения информации о товарах,
    добавленных пользователями в их корзину.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    """ Заказ """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Log(models.Model):
    """
    Модель Log предназначена для хранения записей о действиях,
    выполненных пользователями в системе.
    Каждая запись будет включать информацию о действии, времени его выполнения и пользователе,
    который его совершил.
    """
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"


