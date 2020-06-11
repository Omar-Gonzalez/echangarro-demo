from django.shortcuts import render, redirect
from django.views import View, generic
from carros.models import Carro, ProductoEnCarro
from .forms import AgregaProductoForm, BorraProductoEnCarroForm
from productos.mixins import CategoriaMixin, MarcaMixin
from cms.mixins import ConfigMixin
from perfiles.mixins import PerfilMixin
from productos.models import Producto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .mixins import CarroDeUsuarioMixin
from echangarro.globals import CARRO_VACIO, SIN_EXISTENCIA


class CarroView(LoginRequiredMixin, View, ConfigMixin, CarroDeUsuarioMixin, CategoriaMixin, MarcaMixin, PerfilMixin):
    login_url = '/entra/'

    def get(self, request):
        context = dict()
        self.get_config_data(context)
        self.get_carro_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        self.get_perfil_data(context)
        context.update({
            'prodForm': AgregaProductoForm(),
            'borraForm': BorraProductoEnCarroForm()
        })

        if context['carro'].num_de_productos == 0:
            messages.info(self.request, CARRO_VACIO)
            return redirect('/')

        return render(request, 'carro.html', context)


class AgregaCarroFormView(LoginRequiredMixin, generic.FormView):
    template_name = 'carro.html'
    form_class = AgregaProductoForm
    success_url = '/carro/'
    login_url = '/entra/'

    def form_valid(self, form):
        pk_producto_agregado = form.cleaned_data['pk_producto']
        cantidad = form.cleaned_data['cantidad']
        carro = Carro.objects.filter(user=self.request.user).first()
        producto = Producto.objects.get(pk=pk_producto_agregado)

        if producto.stock <= 0:
            return self.form_invalid(form)

        # El producto ya se encuentra en el carro, updatea cantidad
        for producto_en_carro in carro.productos:
            if producto_en_carro.producto.pk == pk_producto_agregado:
                prod_update = ProductoEnCarro.objects.get(pk=producto_en_carro.pk)
                prod_update.cantidad = prod_update.cantidad + cantidad
                prod_update.save()
                return super().form_valid(form)

        # Producto nuevo se agrega al carro
        nuevo_prod_carro = ProductoEnCarro(
            carro=carro,
            producto=producto,
            cantidad=cantidad)
        nuevo_prod_carro.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, SIN_EXISTENCIA)
        return redirect('/')


class ActualizaCarroFormView(generic.FormView):
    template_name = 'carro.html'
    form_class = AgregaProductoForm
    success_url = '/carro/'

    def form_valid(self, form):
        pk_producto_agregado = form.cleaned_data['pk_producto']
        cantidad = form.cleaned_data['cantidad']
        carro = Carro.objects.filter(user=self.request.user).first()

        for producto_en_carro in carro.productos:
            if producto_en_carro.producto.pk == pk_producto_agregado:
                prod_update = ProductoEnCarro.objects.get(pk=producto_en_carro.pk)
                prod_update.cantidad = cantidad
                prod_update.save()
                return super().form_valid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class BorraProductoEnCarro(generic.FormView):
    template_name = 'carro.html'
    form_class = BorraProductoEnCarroForm
    success_url = '/carro/'

    def form_valid(self, form):
        pk = form.cleaned_data['pk_producto']
        ProductoEnCarro.objects.get(pk=pk).delete()
        return super().form_valid(form)


class CarroAjaxView(View, CarroDeUsuarioMixin):

    def get(self, request):
        context = None
        if request.user.is_authenticated:
            context = dict()
            self.get_carro_data(context)
        return render(request, 'ajax/carro-dropdown.html', context)
