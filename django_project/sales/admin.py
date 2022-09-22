from django.contrib import admin
from .models import Item,Order,OrderItem


class OrderInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra=0

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display=['id','name','price','remind','group','type']
    list_filter=['name']
    search_fields=['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','buyer','total','success']
    list_filter=['success']
    inlines=[OrderInlineAdmin]

   
