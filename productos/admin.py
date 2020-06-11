from django.contrib import admin
from .models import *
from imagenes.models import Imagen


class ImagenInline(admin.TabularInline):
    model = Imagen


class AdminCategoria(admin.ModelAdmin):
    search_fields = [
        'nombre'
    ]

    list_display = [
        'nombre',
        'creado',
        'actualizado'
    ]


admin.site.register(Categoria, AdminCategoria)


class AdminMarca(admin.ModelAdmin):
    search_fields = [
        'nombre'
    ]

    list_display = [
        'nombre',
        'creado',
        'actualizado'
    ]


admin.site.register(Marca, AdminMarca)


class AdminProducto(admin.ModelAdmin):
    search_fields = [
        'nombre'
    ]

    list_display = [
        'nombre',
        'categoria',
        'marca',
        'escala',
        'numero_de_modelo',
        'visible_en_tienda',
        'precio',
        'destacado',
        'categoria_envio',
    ]

    inlines = [
        ImagenInline
    ]


admin.site.register(Producto, AdminProducto)
