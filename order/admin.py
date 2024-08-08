from django.contrib import admin
from .models import Order,OrderItem

# Register your models here.

# admin.site.register((Order,OrderItem))

@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ("id", 'amount', 'user')
    list_filter = ("user", )


@admin.register(OrderItem)
class OrderItemAdminModel(admin.ModelAdmin):
    list_display = ("order_id", 'total')
    list_filter = ("order", )