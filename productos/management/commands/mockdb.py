from django.core.management.base import BaseCommand, CommandError
from productos.models import Categoria, Marca, Producto
import urllib.request
from random import randint
from django.db import IntegrityError

lorems = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam rutrum nibh porttitor orci tempus lobortis. Nunc sollicitudin quam eget tellus mollis, a bibendum ex porta. Aenean ac magna sit amet odio scelerisque viverra ac et neque. Proin congue vehicula egestas. Nunc ac turpis fermentum, viverra orci a, tincidunt ante. Quisque velit quam, fermentum at leo nec, vulputate finibus sapien. Quisque efficitur nisi quis rhoncus iaculis. Mauris et metus purus. Nulla facilisi. Duis tellus ante, ultrices eget nisi eu, blandit lobortis enim. Nam consectetur vestibulum mauris in accumsan.',
    'Sed suscipit efficitur sapien, vestibulum commodo libero convallis eget. Quisque libero dui, malesuada quis cursus eu, dapibus in purus. Sed ullamcorper augue ex, ac ultricies leo ultrices in. Cras varius mi maximus odio ornare ornare. Sed sed purus mi. Donec rutrum porta risus nec rutrum. Proin viverra dictum est vitae convallis. Aliquam erat volutpat. Quisque vitae accumsan nisl. Duis nunc velit, auctor eu augue ac, aliquam pellentesque dui. Ut sit amet urna id metus ornare congue in nec enim. Curabitur fermentum bibendum ligula sit amet fringilla. Fusce nibh leo, varius sit amet tellus at, vulputate porttitor nisl.',
    'Nam tempor est in lacus sollicitudin consectetur. Curabitur tellus massa, aliquam a viverra at, elementum eu nisi. Duis sollicitudin euismod convallis. Nunc euismod et ex sit amet tempor. Sed a cursus mauris, ac interdum felis. Morbi ante tortor, sollicitudin eu dictum non, accumsan nec turpis. Etiam sit amet efficitur libero. Curabitur sit amet bibendum nibh. Cras varius nisl vel feugiat ultrices. Nulla pharetra eros sit amet est semper, sed posuere augue commodo. Pellentesque nec diam vitae nunc tincidunt aliquet ac sit amet augue. Duis pellentesque sed augue eget semper. Morbi a eros ac neque tempor pellentesque. Quisque eget libero leo. Sed consequat interdum tellus at maximus. Phasellus vel diam non magna commodo ultricies.',
    'Nunc volutpat odio ut dui commodo dignissim. Sed lobortis vulputate efficitur. Ut sollicitudin et massa a dignissim. Fusce accumsan non neque ac aliquet. Nulla sollicitudin nec lorem ullamcorper pellentesque. Cras pulvinar metus sed libero eleifend, a consequat lacus ultrices. Donec at nisi nibh. In hac habitasse platea dictumst. Aliquam facilisis elit nec euismod commodo. Nullam eget tortor ut libero iaculis semper quis vitae enim. Aenean luctus commodo ligula, sit amet rhoncus massa sodales posuere. Sed efficitur leo in mi dapibus lobortis. Morbi vitae dapibus libero. Vivamus ut augue tincidunt, pretium urna sit amet, semper elit. Quisque laoreet gravida erat ac suscipit. Aliquam a nulla suscipit lorem interdum rhoncus.'
]


def obten_palabras():
    word_url = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    palabras = long_txt.splitlines()
    return palabras


class Command(BaseCommand):
    help = 'llena una db mock de marcas'

    def add_arguments(self, parser):
        parser.add_argument('argumentos', nargs='+', type=int)

    def handle(self, *args, **options):
        opt = options['argumentos']
        cantidad = int(opt[0])
        max = int(opt[1])
        print(f'Generando : {cantidad} productos')
        print(f'Con maximo rango de marca y categoria de : {max}')
        i = 0
        palabras = obten_palabras()

        while i < opt[0]:
            cat = Categoria.objects.get(pk=randint(1, max))
            marca = Marca.objects.get(pk=randint(1, max))
            try:
                producto = Producto(
                    nombre=palabras[randint(0, len(palabras))],
                    descripcion=lorems[randint(0, len(lorems) - 1)],
                    categoria=cat,
                    marca=marca,
                    stock=randint(1, 300),
                    precio_lista=randint(1, 5000),
                    visible_en_tienda=True,
                    destacado=True
                )
                producto.save()
            except IntegrityError:
                pass
            i = i + 1
