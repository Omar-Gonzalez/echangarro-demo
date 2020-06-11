from django.contrib import admin
from .models import Configuracion, MensajeContacto


class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_tienda',
        'descripcion',
        'aviso_privacidad',
        'terminos_y_condiciones',
        'correo_contacto',
        'direccion_tienda',
        'telefono_contacto',
        'logo_tienda',
        'banner_tienda'
    ]

    def has_add_permission(self, request):
        if Configuracion.objects.all().count() > 0:
            return False
        else:
            return True


admin.site.register(Configuracion, ConfiguracionAdmin)


class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = [
        'usuario_registrado',
        'nombre_de_contacto',
        'correo_electronico',
        'telefono_de_contacto',
        'mensaje',
        'creado'
    ]


admin.site.register(MensajeContacto, MensajeContactoAdmin)
