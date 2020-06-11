from django.db import models
from imagenes.models import Imagen
from envios.models import CategoriaEnvio


class Categoria(models.Model):
    nombre = models.CharField(max_length=220, unique=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria de producto'
        verbose_name_plural = 'Categorias de productos'

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=220, unique=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Marca de producto'
        verbose_name_plural = 'Marcas de productos en tienda'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    ESCALA_CHOICES = (
        ('1/20', '1/20'),
        ('1/24', '1/24'),
        ('1/32', '1/32'),
        ('1/35', '1/35'),
        ('1/48', '1/48'),
        ('1/72', '1/72'),
        ('1/150', '1/150'),
        ('1/350', '1/350'),
        ('1/700', '1/700'),
        ('1/3000', '1/3000'),
    )
    nombre = models.CharField(max_length=220, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, blank=True, null=True)
    escala = models.CharField(max_length=110, choices=ESCALA_CHOICES, blank=True, null=True)
    numero_de_modelo = models.CharField(max_length=110, blank=True, null=True)
    numero_de_piezas = models.IntegerField(blank=True, null=True)
    nivel_de_dificultad = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    visible_en_tienda = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    categoria_envio = models.ForeignKey(CategoriaEnvio, null=True, on_delete=models.SET_NULL)
    precio_lista = models.IntegerField()
    porcentaje_de_descuento = models.IntegerField(null=True, blank=True)
    precio_con_descuento = models.IntegerField(null=True, blank=True)
    leyenda_descuento = models.CharField(max_length=220, null=True, blank=True)

    @property
    def imagen_principal(self):
        return Imagen.objects.filter(producto=self).order_by('orden_de_desplegado').first().imagen

    @property
    def imagenes(self):
        return Imagen.objects.filter(producto=self, activa=True).order_by('orden_de_desplegado')

    @property
    def precio(self):
        if self.precio_con_descuento:
            return self.precio_con_descuento
        if self.porcentaje_de_descuento:
            return round(self.precio_lista - (self.precio_lista * self.porcentaje_de_descuento) / 100, 2)
        return self.precio_lista

    @property
    def ahorro_porcentaje(self):
        porcentaje = 0
        if self.porcentaje_de_descuento:
            porcentaje = self.porcentaje_de_descuento
        if self.precio_con_descuento:
            porcentaje = round(self.ahorro_cantidad * 100 / self.precio_lista, 1)
        return porcentaje

    @property
    def ahorro_cantidad(self):
        return self.precio_lista - self.precio

    @property
    def tiene_descuento(self):
        descuento = False
        if self.porcentaje_de_descuento or self.precio_con_descuento:
            descuento = True
        return descuento

    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre + ' (' + self.categoria.nombre + ')'
