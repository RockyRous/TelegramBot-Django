import django_tables2 as tables
from .models import Order, TelegramUser

class OrderTable(tables.Table):
    order_id = tables.Column(accessor='id', verbose_name='Order ID')
    user_id = tables.Column(verbose_name='User ID')
    user_data = tables.Column(verbose_name='User Data')
    created_at = tables.Column(verbose_name='Date Created')
    total_price = tables.Column(verbose_name='Total Price')
    status = tables.Column(verbose_name='Status')

    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap.html"  # Подключаем стандартный шаблон
        fields = ('order_id', 'user_id', 'user_data', 'created_at', 'total_price', 'status')
