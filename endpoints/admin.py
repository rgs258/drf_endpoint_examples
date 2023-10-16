# Register your models here.

from django.contrib import admin

from .models import Customer, Product, Order, Address, Review

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Review)
