from django.shortcuts import render
from django_tables2 import SingleTableView
from .models import Order
from .tables import OrderTable

class OrderListView(SingleTableView):
    model = Order
    table_class = OrderTable
    template_name = "orders/order_list.html"
