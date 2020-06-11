from django.contrib import admin
from .models import Imagen


class ImagenAdmin(admin.ModelAdmin):
    list_display = [
        'leyenda',
        'imagen',
        'orden_de_desplegado',
        'activa',
        'creado',
        'actualizado'
    ]


admin.site.register(Imagen, ImagenAdmin)
