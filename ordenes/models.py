from django.db import models
from productos.models import Producto
from django.contrib.auth.models import User
from echangarro.globals import PREFERENCIA_PAGO_CHOICES, ESTADO_ORDEN_CHOICES


class Orden(models.Model):
    @property
    def numero(self):
        return self.pk

    user = models.ForeignKey(User, on_delete=models.CharField)
    estado = models.CharField(
        max_length=110,
        default='INICIADO',
        choices=ESTADO_ORDEN_CHOICES
    )

    preferencia_de_pago = models.CharField(
        max_length=110,
        default='MERCADO LIBRE',
        choices=PREFERENCIA_PAGO_CHOICES
    )

    guia_de_envio = models.CharField(max_length=640, blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    @property
    def productos(self):
        return ProductoEnOrden.objects.filter(orden=self).all()

    @property
    def total(self):
        total = 0
        for producto in self.productos:
            total = total + producto.sub_total
        return total

    @property
    def total_con_envio(self):
        costos = []
        for producto in self.productos:
            try:
                costos.append(
                    producto.producto.categoria_envio.costo_envio_nacional)
            except:
                pass
        try:
            return max(costos) + self.total
        except:
            return self.total

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compra'

    def __str__(self):
        return 'Orden(' + str(self.pk) + '): ' + self.user.username


class ProductoEnOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    @property
    def sub_total(self):
        return self.producto.precio * self.cantidad

    class Meta:
        verbose_name_plural = 'Productos en ordenes'
        verbose_name = 'Producto en orden'

    def __str__(self):
        return '({}) {} - sub total: {}'.format(str(self.cantidad), self.producto.nombre, self.sub_total)


class DireccionOrden(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=220)
    colonia = models.CharField(max_length=220)
    municipio = models.CharField(max_length=220)
    codigo_postal = models.IntegerField()
    estado = models.CharField(max_length=110)
    referencias = models.TextField(blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Direccion de envio para orden'
        verbose_name_plural = 'Direcciones de envio para ordenes'

    def __str__(self):
        return self.direccion + ', ' + self.colonia + ' ' + self.municipio + ' - ' + self.estado
