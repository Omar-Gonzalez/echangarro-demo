from django.contrib import admin
from .models import *


class ProductoEnCarroAdmin(admin.ModelAdmin):
    list_display = [
        'carro',
        'producto',
        'cantidad',
        'sub_total',
    ]



class ProductoEnCarroInline(admin.TabularInline):
    model = ProductoEnCarro


class CarroAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'productos_en_carro',
        'total',
    ]

    inlines = [
        ProductoEnCarroInline
    ]


admin.site.register(Carro, CarroAdmin)