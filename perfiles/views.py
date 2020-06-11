from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db import transaction
from django.http.response import HttpResponseRedirect
from .forms import EntraForm, UsuarioNuevoForm, DireccionForm, PerfilForm, ProductoDeseadoForm, \
    RemueveProdDeseadoForm, FotoPerfilForm, GeneraPwdForm, NuevPwdForm
from carros.models import Carro
from carros.forms import AgregaProductoForm
from .models import ProductoDeseado
from productos.models import Producto
from productos.mixins import CategoriaMixin, MarcaMixin
from perfiles.models import Perfil, Direccion
from servicios.mixins import ServiciosDisponiblesMixin
from .mixins import PerfilMixin
from cms.mixins import ConfigMixin
from echangarro.globals import LOGIN_INVALIDO
from .mails import confirma_usuario_con, notificacion_nuevo_usuario, genera_nueva_contraseña
import random
import string


class EntraFormView(generic.FormView, ConfigMixin, CategoriaMixin, MarcaMixin):
    template_name = 'autenticacion/entra.html'
    form_class = EntraForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        return context

    def form_valid(self, form):
        try:
            user = User.objects.get(username=form.cleaned_data['email'])
            perfil = Perfil.objects.get(user=user)
            if perfil.pwd_comprometido:
                messages.error(self.request,
                               'Esta cuenta esta proceso de cambio de password y por lo tanto no puede ser accedida,'
                               ' por favor sigue las instrucciones en tu correo de recuperacion de cuenta')
                return redirect('/entra/')
        except Perfil.DoesNotExist:
            pass
        except User.DoesNotExist:
            pass
        username = form.cleaned_data['email']
        password = form.cleaned_data['contraseña']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, LOGIN_INVALIDO)
        return super().form_invalid(form)


class UsuarioNuevoFormView(generic.FormView, ConfigMixin, MarcaMixin, CategoriaMixin):
    template_name = 'autenticacion/usuario-nuevo.html'
    form_class = UsuarioNuevoForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def form_valid(self, form):
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    user = User.objects.get(email=form.cleaned_data['email'])
                    carro = Carro(user=user)
                    carro.save()
                    perfil = Perfil(user=user)
                    perfil.save()
                login(self.request, user)
                try:
                    confirma_usuario_con(user.username, self.request.get_host(), perfil.uuid_de_confirmacion)
                    notificacion_nuevo_usuario(user.username)
                except Exception as e:
                    print(e)
                return super().form_valid(form)
            except:
                messages.error(self.request, 'Algo salio mal, por favor intenta de nuevo')
                return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def cierra_sesion(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def confirma_correo_de_usuario(request, uuid):
    try:
        perfil = Perfil.objects.get(uuid_de_confirmacion=uuid)
        if perfil.correo_confirmado:
            messages.warning(request, f'{perfil.correo} ya habia sido confirmado, no es necesario confirmarlo de nuevo')
        else:
            perfil.correo_confirmado = True
            perfil.save()
            messages.success(request, f'¡Hemos confirmado tu correo {perfil.correo} con exito!')
    except Perfil.DoesNotExist:
        messages.error(request, 'El perfil del correo que se esta tratando de confirmar no existe')
        pass
    return redirect('/perfil/')


class PerfilUsuarioTemplateView(LoginRequiredMixin, generic.TemplateView, PerfilMixin,
                                ConfigMixin, MarcaMixin, CategoriaMixin, RemueveProdDeseadoForm, ServiciosDisponiblesMixin):
    login_url = '/entra/'
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        self.get_perfil_data(context)
        context.update({
            'perfilDisponible': not self.perfil_desabilitado,
            'remueveForm': RemueveProdDeseadoForm(),
            'agregaForm': AgregaProductoForm(),
        })
        return context


class DireccionUsuarioFormView(LoginRequiredMixin, generic.FormView, ConfigMixin):
    login_url = '/entra/'
    success_url = '/perfil/'
    form_class = DireccionForm
    template_name = 'formas/perfil-forma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        return context

    def form_valid(self, form):
        if form.is_valid():
            perfil = Perfil.objects.get(user=self.request.user)
            form.instance.perfil = perfil
            form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid()


class DireccionCreateView(LoginRequiredMixin, generic.CreateView, ConfigMixin, CategoriaMixin,
                          MarcaMixin):
    login_url = '/entra/'
    form_class = DireccionForm
    model = Direccion
    template_name = 'formas/perfil-forma.html'
    success_url = '/perfil/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def form_valid(self, form):
        if form.is_valid():
            perfil = Perfil.objects.get(user=self.request.user)
            form.instance.perfil = perfil
            form.save()
        return super().form_valid(form)


class DireccionUpdateView(LoginRequiredMixin, generic.UpdateView, ConfigMixin, MarcaMixin,
                          CategoriaMixin):
    login_url = '/entra/'
    success_url = '/perfil/'
    form_class = DireccionForm
    template_name = 'formas/perfil-forma.html'
    model = Direccion

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        direccion = Direccion.objects.get(pk=self.kwargs['pk'])
        perfil = Perfil.objects.get(user=self.request.user)
        if perfil != direccion.perfil:
            # TODO:Agrega mensaje : forma de otro usurio
            context.update({
                'form': None
            })
        self.get_config_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        return context


class DireccionDeleteView(LoginRequiredMixin, generic.DeleteView, ConfigMixin, CategoriaMixin,
                          MarcaMixin):
    model = Direccion
    success_url = '/perfil/'
    login_url = '/entra/'
    template_name = 'formas/perfil-confirma-eliminar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        perfil = Perfil.objects.get(user=self.request.user)
        if self.request.user != perfil.user:
            # TODO:Agrega mensaje : forma de otro usurio
            context.update({
                'form': None
            })
        self.get_config_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        return context


class PerfilInfoUpdateView(LoginRequiredMixin, generic.UpdateView, ConfigMixin, MarcaMixin,
                           CategoriaMixin):
    login_url = '/entra/'
    template_name = 'formas/perfil-forma.html'
    form_class = PerfilForm
    model = Perfil
    success_url = '/perfil/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        perfil = Perfil.objects.get(user=self.request.user)
        if self.request.user != perfil.user:
            # TODO:Agrega mensaje : forma de otro usurio
            context.update({
                'form': None
            })
        self.get_config_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context


class AddProductoDeseadoFormView(LoginRequiredMixin, generic.FormView):
    login_url = '/entra/'
    form_class = ProductoDeseadoForm

    def form_valid(self, form):
        if form.is_valid():
            prod = Producto.objects.get(pk=form.cleaned_data['pk_producto'])
            prod_deseado = ProductoDeseado()
            prod_deseado.user = self.request.user
            prod_deseado.producto = prod
            prod_deseado.save()
            messages.success(self.request, f'{prod.nombre} agregado exitosamente a tu lista de productos deseados')
        return HttpResponseRedirect(form.cleaned_data['next'])

    def form_invalid(self, form):
        messages.error(self.request, 'Lo sentimos no se pudo agregar el producto a tu lista de deseados')
        return HttpResponseRedirect(form.cleaned_data['next'])


class RemueveProductoDeseadoFormView(LoginRequiredMixin, generic.FormView):
    login_url = '/entra/'
    form_class = RemueveProdDeseadoForm

    def form_valid(self, form):
        print('form valid')
        if form.is_valid():
            try:
                ProductoDeseado.objects.filter(user=self.request.user,
                                               producto=form.cleaned_data['pk_producto']).delete()
                messages.success(self.request, 'Producto removido exitosamente a tu lista de productos deseados')
            except ProductoDeseado.DoesNotExist:
                messages.error(self.request, 'Lo sentimos no se pudo remover el producto a tu lista de deseados')
        return HttpResponseRedirect('/perfil/')

    def form_invalid(self, form):
        messages.error(self.request, 'Lo sentimos no se pudo remover el producto a tu lista de deseados')
        return HttpResponseRedirect('/perfil/')


class FotoPerfilFormView(generic.FormView, LoginRequiredMixin, PerfilMixin, ConfigMixin, MarcaMixin,
                         CategoriaMixin):
    login_url = '/entra/'
    template_name = 'formas/perfil-foto-forma.html'
    success_url = '/perfil/'
    success_mesage = 'Hemos guardad tu nueva foto de perfil con exito'
    form_class = FotoPerfilForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_categoria_data(context)
        self.get_marca_data(context)
        self.get_perfil_data(context)
        return context

    def form_invalid(self, form):
        messages.error(self.request,
                       'El archivo que subiste no es valido, por favor intenta con un archivo de formato de imagen valido')
        return super().form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data['foto_de_perfil'] == None:
            messages.error(self.request, 'Por favor seleciona una foto antes de guardar la forma')
            return super().form_invalid(form)
        perfil = Perfil.objects.get(user=self.request.user)
        perfil.foto_de_perfil = form.cleaned_data['foto_de_perfil']
        perfil.save()
        messages.success(self.request, 'Hemos guardado tu nueva foto de perfil con exito')
        return super().form_valid(form)


class GeneraPwdFormView(generic.FormView, PerfilMixin, ConfigMixin, MarcaMixin,
                        CategoriaMixin):
    template_name = 'formas/genera-pwd-forma.html'
    form_class = GeneraPwdForm
    success_url = '/'

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = User.objects.get(username=form.cleaned_data['correo_de_cuenta'])
                perfil = Perfil.objects.get(user=user)
                perfil.pwd_comprometido = True
                perfil.save()
                user.set_password(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)))
                user.save()
            genera_nueva_contraseña(user.username, self.request.get_host(), perfil.uuid_de_confirmacion)
            messages.success(self.request,
                             'Hemos enviado un correo de recuperacion de contraseña, por favor sigue las instrucciones proporcionadas')
        except User.DoesNotExist:
            pass
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class NuevoPwdFormView(generic.FormView, PerfilMixin, ConfigMixin, MarcaMixin,
                        CategoriaMixin):
    template_name = 'formas/nuevo-pwd-forma.html'
    form_class = NuevPwdForm
    success_url = '/entra/'

    def get(self, request, *args, **kwargs):
        try:
            perfil = Perfil.objects.get(uuid_de_confirmacion=kwargs['uuid'])
            if perfil.pwd_comprometido == False:
                return HttpResponseForbidden()
        except Perfil.DoesNotExist:
            return HttpResponseForbidden()
        return super(NuevoPwdFormView, self).get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if form.cleaned_data['nueva_contraseña'] == form.cleaned_data['verifica_contraseña']:
            try:
                with transaction.atomic():
                    perfil = Perfil.objects.get(uuid_de_confirmacion=self.kwargs['uuid'])
                    perfil.pwd_comprometido = False
                    user = User.objects.get(username=perfil.correo)
                    user.set_password(form.cleaned_data['nueva_contraseña'])
                    user.save()
                    perfil.save()
                messages.success(self.request, 'Se ha guardado tu contraseña con exito, puedes entrar con tu nueva contraseña:')
            except:
                messages.error(self.request,
                               'Error interno, por favor intenta de nuevo')
                return super().form_invalid(form)
        else:
            messages.error(self.request, 'Tu nueva contraseña y verificación no coinciden, por favor intenta de nuevo')
            return super().form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CambioDePwdFormView(generic.FormView, LoginRequiredMixin, PerfilMixin, ConfigMixin, MarcaMixin,
                        CategoriaMixin):

    template_name = 'formas/nuevo-pwd-forma.html'
    form_class = NuevPwdForm
    success_url = '/entra/'
    login_url = '/entra/'

    def form_valid(self, form):
        if form.cleaned_data['nueva_contraseña'] == form.cleaned_data['verifica_contraseña']:
            try:
                user = User.objects.get(username=self.request.user.username)
                user.set_password(form.cleaned_data['nueva_contraseña'])
                user.save()
            except User.DoesNotExist:
                messages.error(self.request, 'Error interno, por favor intenta de nuevo más tarde')
                return super().form_invalid(form)
                pass
        else:
            messages.error(self.request, 'Tu nueva contraseña no coincide con la verificación, por favor intenta de nuevo')
            return super().form_invalid(form)
        messages.success(self.request, 'Hemos actualizado tu password con exito, por favor entra con tu nuevo password.')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)