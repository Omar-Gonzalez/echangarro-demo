from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


# Create your models here.
class Configuracion(models.Model):
    nombre_tienda = models.CharField(max_length=220)
    descripcion = models.TextField(blank=True, null=True)
    aviso_privacidad = models.TextField(blank=True, null=True)
    terminos_y_condiciones = models.TextField(blank=True, null=True)
    correo_contacto = models.CharField(max_length=110, blank=True, null=True)
    direccion_tienda = models.TextField(blank=True, null=True)
    telefono_contacto = models.CharField(max_length=110, blank=True, null=True)
    logo_tienda = ImageField(null=True, blank=True)
    banner_tienda = ImageField(null=True, blank=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    @property
    def mostrar_datos_de_contacto(self):
        if self.correo_contacto or self.direccion_tienda or self.telefono_contacto:
            return True
        return False

    class Meta:
        verbose_name = 'Configuracion de tienda'
        verbose_name_plural = 'Configuracion de datos de tienda'

    def __str__(self):
        return self.nombre_tienda


class MensajeContacto(models.Model):
    usuario_registrado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_de_contacto = models.CharField(max_length=110, blank=True, null=True)
    correo_electronico = models.EmailField()
    telefono_de_contacto = models.CharField(max_length=110, blank=True, null=True)
    mensaje = models.TextField()
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Mensaje de contacto de cliente'
        verbose_name_plural = 'Mensajes enviados por clientes'

    def __str__(self):
        return self.mensaje
