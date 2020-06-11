from django.db import models
from sorl.thumbnail import ImageField


class Imagen(models.Model):
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    orden_de_desplegado = models.IntegerField()
    imagen = ImageField()
    leyenda = models.CharField(max_length=110, blank=True, null=True)
    activa = models.BooleanField(default=True)

    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imagenes de producto'

    def __str__(self):
        return f'{self.producto.nombre} - orden de desplegado: f{self.orden_de_desplegado}'
