from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """ Категории
    Модель Category используется для создания иерархии категорий товаров.
    Она может иметь родительскую категорию, что позволяет создавать подкатегории.
    """
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name


def validate_image_size(image):
    MAX_SIZE = 5 * 1024 * 1024  # 5 МБ
    if image.size > MAX_SIZE:
        raise ValidationError(f"Размер изображения не должен превышать {MAX_SIZE / (1024 * 1024)} MB")


class Product(models.Model):
    """ Продукт """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True, validators=[validate_image_size])
    # todo будем загружать юрл на картинку и хранить строку

    def __str__(self):
        return self.name


class CartItem(models.Model):
    """
    Модель CartItem используется для хранения информации о товарах,
    добавленных пользователями в их корзину.
    """
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    """ Заказ """
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class Log(models.Model):
    """
    Модель Log предназначена для хранения записей о действиях,
    выполненных пользователями в системе.
    Каждая запись будет включать информацию о действии, времени его выполнения и пользователе,
    который его совершил.
    """
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action} | {self.user}"


