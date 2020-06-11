from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from echangarro.globals import ESTADOS_MEXICO
from sorl.thumbnail import ImageField
import uuid


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=220, blank=True, null=True)
    apeidos = models.CharField(max_length=220, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    telefono_alternativo = models.CharField(max_length=20, blank=True, null=True)
    foto_de_perfil = ImageField(blank=True, null=True)
    correo_confirmado = models.BooleanField(default=False)
    pwd_comprometido = models.BooleanField(default=False)
    uuid_de_confirmacion = models.UUIDField(default=uuid.uuid4, editable=False)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    @property
    def correo(self):
        try:
            return User.objects.get(pk=self.user.pk)
        except User.DoesNotExist:
            return 'N.A.'

    @property
    def direcciones_registradas(self):
        return Direccion.objects.filter(perfil=self).count()

    @property
    def tiene_info_contacto(self):
        if self.nombre is not None and self.apeidos is not None and self.telefono is not None:
            return True
        return False

    @property
    def tiene_direccion(self):
        if self.direcciones_registradas > 0:
            return True
        return False

    @property
    def completo(self):
        if self.tiene_direccion and \
                self.tiene_info_contacto is not False and \
                self.uuid_de_confirmacion is not False:
            return True
        return False

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        return self.user.username + ' - ' + self.user.email


class Direccion(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=220)
    colonia = models.CharField(max_length=220)
    municipio = models.CharField(max_length=220)
    codigo_postal = models.IntegerField()
    estado = models.CharField(choices=ESTADOS_MEXICO, max_length=110)
    referencias = models.TextField(blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Direccion de usuario'
        verbose_name_plural = 'Direcciones de usuario'

    def __str__(self):
        return self.direccion + ', ' + self.colonia + ' ' + self.municipio + ' - ' + self.estado


class ProductoDeseado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
