from django.contrib import admin
from .models import Order, OrderItem, User, Product

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Product)
