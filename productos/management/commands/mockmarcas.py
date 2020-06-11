from django.core.management.base import BaseCommand, CommandError
from productos.models import Marca
from .mockdb import obten_palabras
from random import randint


class Command(BaseCommand):
    help = 'llena una db mock de marcas'

    def add_arguments(self, parser):
        parser.add_argument('cantidad', nargs='+', type=int)

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        print(f'Generando : {cantidad[0]} marcas')
        i = 0
        palabras = obten_palabras()

        while i < cantidad[0]:
            marca = Marca(nombre=palabras[randint(0, len(palabras))])
            marca.save()
            i = i + 1
