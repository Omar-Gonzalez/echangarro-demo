from django.contrib import admin
from .models import CategoriaEnvio


class CategoriaEnvioAdmin(admin.ModelAdmin):
    readonly_fields = [
        'identificador',
        'descripcion',
        'dimensiones_maximas',
        'necesario_cotizar',
        'creado',
        'actualizado',
    ]

    list_display = [
        'identificador',
        'descripcion',
        'costo_envio_nacional',
    ]


admin.site.register(CategoriaEnvio, CategoriaEnvioAdmin)