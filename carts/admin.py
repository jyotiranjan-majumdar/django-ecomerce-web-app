from django.contrib import admin

from .models import Cart
from .models import CartItem
from .models import Product 
#Register your models here.

class CartAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)

admin.site.register(CartItem, CartAdmin)

