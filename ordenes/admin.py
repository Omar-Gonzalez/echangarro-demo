from django.contrib import admin
from .models import Orden, ProductoEnOrden, DireccionOrden


class ProductoEnOrdenAdmin(admin.ModelAdmin):
    readonly_fields = [
        'orden',
        'sub_total'
    ]
    list_display = [
        'producto',
        'cantidad',
    ]


class ProductoEnOrdenInline(admin.TabularInline):
    model = ProductoEnOrden


class DireccionEnOrdenInline(admin.TabularInline):
    model = DireccionOrden


class AdminOrden(admin.ModelAdmin):
    readonly_fields = [
        'numero',
        'total'
    ]
    list_display = [
        'user',
        'numero',
        'estado',
        'preferencia_de_pago',
        'guia_de_envio',
        'total'
    ]

    inlines = [
        ProductoEnOrdenInline,
        DireccionEnOrdenInline
    ]


admin.site.register(Orden, AdminOrden)


class DireccionOrdenAdmin(admin.ModelAdmin):
    readonly_fields = [
        'orden'
    ]

    list_display = [
        'direccion',
        'colonia',
        'municipio',
        'codigo_postal',
        'estado',
        'referencias',
        'creado',
        'actualizado'
    ]


admin.site.register(DireccionOrden, DireccionOrdenAdmin)
