from django.db import models


class CategoriaEnvio(models.Model):
    PROVEEDORES = (
        ('DHL', 'DHL'),
        ('ESTAFETA', 'ESTAFETA'),
        ('UPS', 'UPS'),
        ('CORREO NACIONAL', 'CORREO NACIONAL'),
    )

    CATEGORIAS = (
        ('SOBRE CHICO', 'SOBRE CHICO'),
        ('SOBRE MEDIANO', 'SOBRE MEDIANO'),
        ('SOBRE GRANDE', 'SOBRE GRANDE'),
        ('CAJA EXTRA CHICA', 'CAJA EXTRA CHICA'),
        ('CAJA CHICA', 'CAJA CHICA'),
        ('CAJA MEDIANA', 'CAJA MEDIANA'),
        ('CAJA GRANDE', 'CAJA GRANDE'),
        ('CAJA EXTRA GRANDE', 'CAJA EXTRA GRANDE'),
        ('DIMENSIONES EXTRAORDINARIAS', 'DIMENSIONES EXTRAORDINARIAS'),
    )

    DIMENSIONES = {
        'SOBRE CHICO': '24cm x 12cm',
        'SOBRE MEDIANO': '32cm x 24cm',
        'SOBRE GRANDE': '48cm x 32cm',
        'CAJA EXTRA CHICA': '12cm x 12cm x 12cm',
        'CAJA CHICA': '24cm x 24cm x 24cm',
        'CAJA MEDIANA': '48cm x 48cm x 48cm',
        'CAJA GRANDE': '68cm x 68cm x 68cm',
        'CAJA EXTRA GRANDE': '98cm x 98cm x 98cm',
        'DIMENSIONES EXTRAORDINARIAS': 'DIMENSIONES EXTRAORDINARIAS',
    }

    identificador = models.TextField(max_length=110)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=110, choices=CATEGORIAS, default='CAJA CHICA')
    dimensiones_maximas = models.CharField(max_length=110)
    envio_por = models.CharField(max_length=110, default='DHL', choices=PROVEEDORES)
    costo_envio_nacional = models.IntegerField()
    necesario_cotizar = models.BooleanField(default=False)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.dimensiones_maximas = self.DIMENSIONES[self.categoria]
        self.necesario_cotizar = True if self.categoria == 'DIMENSIONES EXTRAORDINARIAS' else False
        dimensiones_maximas = 'NECESARIO COTIZAR' if self.categoria == 'DIMENSIONES EXTRAORDINARIAS' else self.dimensiones_maximas
        # extra primera letra de categorias para crear iniciales de categoria en identificador
        words = self.categoria.split()
        letters = [word[0] for word in words]
        categoria = "".join(letters)
        self.identificador = f'{categoria}-{self.envio_por}-({self.dimensiones_maximas})'
        self.descripcion = f'{self.categoria}-{self.envio_por}-Dimensiónes máximas:({dimensiones_maximas})-Costo envio nacional: ${self.costo_envio_nacional}'
        super(CategoriaEnvio, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria de envio'
        verbose_name_plural = 'Categorias de envios'

    def __str__(self):
        return self.identificador
