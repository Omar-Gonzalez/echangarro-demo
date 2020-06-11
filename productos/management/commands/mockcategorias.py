from django.core.management.base import BaseCommand, CommandError
from productos.models import Categoria
from .mockdb import obten_palabras
from random import randint


class Command(BaseCommand):
    help = 'llena una db mock de categorias'

    def add_arguments(self, parser):
        parser.add_argument('cantidad', nargs='+', type=int)

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        print(f'Generando : {cantidad[0]} categorias')
        i = 0
        palabras = obten_palabras()

        while i < cantidad[0]:
            cat = Categoria(nombre=palabras[randint(0, len(palabras))])
            cat.save()
            i = i + 1
