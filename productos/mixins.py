from .models import Categoria, Marca


class CategoriaMixin(object):
    def get_categoria_data(self, context):
        categorias = Categoria.objects.all()
        context.update({
            'categorias': categorias
        })
        return context


class MarcaMixin(object):
    def get_marca_data(self, context):
        marcas = Marca.objects.all()
        context.update({
            'marcas': marcas
        })
        return context