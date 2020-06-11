from django.contrib import admin
from .models import *


class PerfilAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'nombre',
        'correo',
        'foto_de_perfil',
        'apeidos',
        'direcciones_registradas',
        'telefono',
        'telefono_alternativo',
        'completo',
        'creado',
        'actualizado'
    ]


admin.site.register(Perfil, PerfilAdmin)


class DireccionAdmin(admin.ModelAdmin):
    list_display = [
        'direccion',
        'colonia',
        'municipio',
        'estado',
        'codigo_postal',
        'creado',
        'actualizado'
    ]


admin.site.register(Direccion, DireccionAdmin)


class ProductoDeseadoAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'producto',
    ]

admin.site.register(ProductoDeseado, ProductoDeseadoAdmin)