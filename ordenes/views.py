from django.shortcuts import render, redirect
from django.views import View
from cms.mixins import ConfigMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from perfiles.forms import DireccionForm, PerfilForm
from perfiles.models import Perfil, Direccion
from .mails import notifica_creacion_de_orden
from .mixins import GuardaOrdenMixin
from .models import Orden
from .forms import SelDireccionForm, ConfirmaOrdenForm
from carros.mixins import CarroDeUsuarioMixin
from servicios.mixins import ServiciosDisponiblesMixin


class PreparaOrdenView(LoginRequiredMixin, View, ConfigMixin, GuardaOrdenMixin, CarroDeUsuarioMixin):
    login_url = '/entra/'

    def get(self, request):
        if request.META.get('HTTP_REFERER') == None:
            # Bloquea path para request que no sean link de carro
            return redirect('/carro/')

        context = dict()
        self.get_config_data(context)

        user = request.user
        perfil = Perfil.objects.get(user=user)
        agrega_dir = False

        if not perfil.tiene_info_contacto:
            form = PerfilForm()

        if not perfil.tiene_direccion:
            form = DireccionForm()

        if not perfil.tiene_info_contacto and not perfil.tiene_direccion:
            messages.info(self.request, 'Por favor agrega la dirección de envio para tu orden')
        if perfil.tiene_direccion and not perfil.tiene_info_contacto:
            messages.info(self.request, 'Por favor agrega tus datos de contacto (nombre y teléfono)')

        if perfil.completo and perfil.direcciones_registradas > 0:
            agrega_dir = True
            form = SelDireccionForm(Direccion.objects.filter(perfil=perfil))

        context.update({
            'perfil': perfil,
            'form': form,
            'agrega': agrega_dir
        })

        return render(request, 'formas/prepara_orden.html', context)

    def post(self, request):
        user = request.user
        perfil = Perfil.objects.get(user=user)

        if not perfil.tiene_info_contacto:
            form = PerfilForm(request.POST)
            if form.is_valid():
                perfil.nombre = form.cleaned_data['nombre']
                perfil.apeidos = form.cleaned_data['apeidos']
                perfil.telefono = form.cleaned_data['telefono']
                perfil.telefono_alternativo = form.cleaned_data['telefono_alternativo']
                perfil.save()

        if not perfil.tiene_direccion:
            form = DireccionForm(request.POST)
            if form.is_valid():
                direccion = Direccion(
                    perfil=perfil,
                    direccion=form.cleaned_data['direccion'],
                    colonia=form.cleaned_data['colonia'],
                    municipio=form.cleaned_data['municipio'],
                    codigo_postal=form.cleaned_data['codigo_postal'],
                    estado=form.cleaned_data['estado'],
                    referencias=form.cleaned_data['referencias']
                )
                direccion.save()

        if perfil.completo and perfil.direcciones_registradas >= 1:
            form = SelDireccionForm(Direccion.objects.filter(perfil=perfil), request.POST)
            if form.is_valid():
                direccion = Direccion.objects.get(pk=form.cleaned_data['direccion_de_envio'])
                self.save_orden(direccion, self.carro, 'TENTATIVA')
                return redirect('/carro/confirma-datos/')

        return redirect('/carro/prepara-orden/')


class ConfirmaDatosView(LoginRequiredMixin, View, ConfigMixin, CarroDeUsuarioMixin, ServiciosDisponiblesMixin):
    login_url = '/entra/'

    def get(self, request):
        if request.META.get('HTTP_REFERER') == None:
            # Bloquea path para request que no sean link de carro
            return redirect('/carro/')

        context = dict()
        context = self.get_config_data(context)
        orden = Orden.objects.filter(user=self.request.user, estado='TENTATIVA').last()
        perfil = Perfil.objects.get(user=self.request.user)
        context.update({
            'ordenesDisponibles': not self.ordenes_desabilitado,
            'orden': orden,
            'perfil': perfil,
            'form': ConfirmaOrdenForm()
        })
        return render(request, 'formas/confirma-orden.html', context)

    def post(self, request):
        form = ConfirmaOrdenForm(request.POST)
        if form.is_valid():
            orden = Orden.objects.filter(user=self.request.user, estado='TENTATIVA').first()
            orden.estado = 'PENDIENTE PAGO'
            orden.preferencia_de_pago = form.cleaned_data['preferencia_de_pago']
            orden.save()
            notifica_creacion_de_orden(orden)
            for producto in self.carro.productos:
                producto.delete()
            return redirect('/perfil/')

        # todo: la probabilidad de una exception es minima, pero hay que manejarla
        return redirect('/perfil/')
