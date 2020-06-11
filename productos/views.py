from django.views import generic
from productos.models import Producto, Categoria, Marca
from .mixins import CategoriaMixin, MarcaMixin
from servicios.mixins import ServiciosDisponiblesMixin
from cms.mixins import ConfigMixin
from perfiles.mixins import PerfilMixin
from carros.forms import AgregaProductoForm
from django.db.models import Q
from perfiles.mixins import PerfilCompletoMixin
from perfiles.forms import ProductoDeseadoForm
from perfiles.models import ProductoDeseado


class ProductosListView(generic.ListView, ConfigMixin, CategoriaMixin, MarcaMixin, PerfilCompletoMixin, PerfilMixin,
                        ServiciosDisponiblesMixin):
    model = Producto
    context_object_name = 'productos'
    template_name = 'productos.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        self.get_perfil_data(context)
        self.verifica_perfil()
        context.update({
            'agregaForm': AgregaProductoForm(),
            'inventarioDisponible': not self.inventario_desabilitado
        })

        return context

    def get_queryset(self):

        if self.request.path == '/ofertas/':
            return Producto.objects.filter(
                Q(visible_en_tienda=True, porcentaje_de_descuento__isnull=False) |
                Q(visible_en_tienda=True, precio_con_descuento__isnull=False)
                ).order_by('precio_lista')

        if self.request.path == '/marcas/':
            return Producto.objects.filter(visible_en_tienda=True).order_by('marca')

        if self.request.path == '/categorias/':
            return Producto.objects.filter(visible_en_tienda=True).order_by('categoria')

        try:
            if self.kwargs['busqueda']:
                return Producto.objects.filter(
                    Q(nombre__icontains=self.kwargs['busqueda']) |
                    Q(categoria__nombre__icontains=self.kwargs['busqueda']) |
                    Q(marca__nombre__icontains=self.kwargs['busqueda'])
                )
        except KeyError:
            pass

        try:
            categoria = self.kwargs['categoria']
            try:
                categoria = Categoria.objects.get(nombre__iexact=categoria)
            except Categoria.DoesNotExist:
                categoria = None
            return Producto.objects.filter(categoria=categoria)
        except KeyError:
            pass

        try:
            marca = self.kwargs['marca']
            try:
                marca = Marca.objects.get(nombre__iexact=marca)
            except Marca.DoesNotExist:
                marca = None
            return Producto.objects.filter(marca=marca)
        except KeyError:
            pass

        try:
            escala = self.kwargs['escala']
            escala = escala.replace(':', '/')
            return Producto.objects.filter(escala=escala).order_by('precio_lista')
        except KeyError:
            pass

        return Producto.objects.filter(visible_en_tienda=True).order_by('precio_lista')


class ProductoDetalleListView(generic.ListView, ConfigMixin, CategoriaMixin, MarcaMixin, PerfilCompletoMixin,
                              PerfilMixin, ServiciosDisponiblesMixin):
    model = Producto
    context_object_name = 'producto'
    template_name = 'detalle.html'

    def es_producto_deseado(self, producto):
        prods_deseados = None
        if self.request.user.is_authenticated:
            try:
                prods_deseados = ProductoDeseado.objects.filter(user=self.request.user)
            except ProductoDeseado.DoesNotExist:
                pass

            for prod_deseado in prods_deseados:
                if prod_deseado.producto.pk == producto.pk:
                    return True
            return False
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        self.verifica_perfil()
        self.get_perfil_data(context)
        context.update({
            'es_producto_deseado': self.es_producto_deseado(context['producto']),
            'agregaForm': AgregaProductoForm(),
            'productoDeseadoForm': ProductoDeseadoForm()
        })
        return context

    def get_queryset(self):
        if self.inventario_desabilitado:
            return []

        try:
            return Producto.objects.get(nombre__iexact=self.kwargs['producto'])
        except Producto.DoesNotExist:
            pass
