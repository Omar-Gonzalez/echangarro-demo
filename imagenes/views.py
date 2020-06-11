from productos.models import Producto
from django.views import generic


class ImgDetalleTemplateView(generic.TemplateView):
    template_name = 'ajax/imagen-detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'prod': Producto.objects.get(pk=kwargs['prod_pk']),
            'img_pk': kwargs['img_pk']
        })
        return context
