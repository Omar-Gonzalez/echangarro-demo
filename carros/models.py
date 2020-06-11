from django.db import models
from productos.models import Producto
from django.utils.html import format_html
from django.contrib.auth.models import User


class Carro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def productos(self):
        return ProductoEnCarro.objects.filter(carro=self).all()

    @property
    def total(self):
        total = 0
        for producto_en_carro in self.productos:
            total += producto_en_carro.sub_total
        return total

    @property
    def productos_en_carro(self):
        lista = ''
        for producto_en_carro in self.productos:
            lista += '<li><a>' + producto_en_carro.producto.nombre + ' - (' + str(
                producto_en_carro.cantidad) + ')</a></li>'
        return format_html(lista)

    @property
    def num_de_productos(self):
        return self.productos.count()


    class Meta:
        verbose_name = 'Carro de compra por usuario'
        verbose_name_plural = 'Carros de compra por usuarios'

    def __str__(self):
        return self.user.username


class ProductoEnCarro(models.Model):
    carro = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='+',
    )

    cantidad = models.IntegerField(default=0)

    @property
    def sub_total(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return self.producto.nombre