from django.db import models


class TelegramUser(models.Model):
    """ Модель хранения базы пользователей """
    user_id = models.IntegerField()


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
    image_url = models.CharField(max_length=255, null=True, blank=True)  # Тут хорошо бы сделать валидацию

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
    user_data = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order {self.id} by {self.user_id}"


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
        return f"{self.timestamp} - {self.action} | {self.user_id}"


class Newsletter(models.Model):
    """ Модель для рассылок """
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_sent = models.BooleanField(default=False)  # Статус рассылки (отправлено или нет)

    def __str__(self):
        return f"Рассылка: {self.title}"


