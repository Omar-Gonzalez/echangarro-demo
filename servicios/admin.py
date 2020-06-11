from django.contrib import admin
from .models import ServiciosDisponibles


class ServiciosDisponiblesAdmin(admin.ModelAdmin):
    list_display = [
        'inventario_disponible',
        'ordenes',
        'cotizacion_envios',
        'creado',
        'actualizado'
    ]

    def has_add_permission(self, request):
        if ServiciosDisponibles.objects.all().count() > 0:
            return False
        else:
            return True


admin.site.register(ServiciosDisponibles, ServiciosDisponiblesAdmin)
