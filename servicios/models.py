from django.db import models


class ServiciosDisponibles(models.Model):
    inventario_disponible = models.BooleanField(default=True)
    perfil_disponible = models.BooleanField(default=True)
    ordenes = models.BooleanField(default=True)
    cotizacion_envios = models.BooleanField(default=True)

    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Servicios disponibles'
        verbose_name_plural = 'Servicio disponibles'