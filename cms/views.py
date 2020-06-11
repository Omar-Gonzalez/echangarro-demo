from django.views import generic
from django.contrib import messages
from django.shortcuts import render_to_response
from .mixins import ConfigMixin
from perfiles.mixins import PerfilMixin
from perfiles.models import Perfil
from productos.mixins import CategoriaMixin, MarcaMixin
from .forms import MansajeContactoForm, MensajeContacto
from .mails import notificacion_error, notificacion_500


def error500(request):
    err_code = 500
    response = render_to_response('errores/500.html', {"code": err_code})
    response.status_code = 500
    notificacion_500(request.build_absolute_uri())
    return response


class Error404TemplateView(generic.TemplateView, ConfigMixin, PerfilMixin, CategoriaMixin, MarcaMixin):
    template_name = 'errores/404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_perfil_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            nombre_tienda = context['config'].nombre_tienda
        except:
            nombre_tienda = 'echangarro-generico'
        notificacion_error('404', request.build_absolute_uri())
        return self.render_to_response(context, status=404)


class Error403TemplateView(generic.TemplateView, ConfigMixin, PerfilMixin, CategoriaMixin, MarcaMixin):
    template_name = 'errores/403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_perfil_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            nombre_tienda = context['config'].nombre_tienda
        except:
            nombre_tienda = 'Tanquemania'
        notificacion_error('404', request.build_absolute_uri())
        return self.render_to_response(context, status=403)


class PrivacidadTemplateView(generic.TemplateView, ConfigMixin, PerfilMixin, CategoriaMixin, MarcaMixin):
    template_name = 'aviso-privacidad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_perfil_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class TerminosTemplateView(generic.TemplateView, ConfigMixin, PerfilMixin, CategoriaMixin, MarcaMixin):
    template_name = 'terminos-condiciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_perfil_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class ContactoTemplateFormView(generic.FormView, ConfigMixin, PerfilMixin, CategoriaMixin, MarcaMixin):
    template_name = 'contacto.html'
    form_class = MansajeContactoForm
    success_url = '/contacto/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.get_config_data(context)
        self.get_perfil_data(context)
        self.get_marca_data(context)
        self.get_categoria_data(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         'Tu mensaje ha sido enviado con exito, nos pondremos en contacto contigo proximamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.user.is_authenticated:
            perfil = None
            try:
                perfil = Perfil.objects.get(user=self.request.user)
            except Perfil.DoesNotExist:
                pass
            if perfil and perfil.completo:
                mensaje = MensajeContacto(
                    usuario_registrado=self.request.user,
                    nombre_de_contacto=f'{perfil.nombre} {perfil.apeidos}',
                    correo_electronico=self.request.user.username,
                    telefono_de_contacto=perfil.telefono,
                    mensaje=form.cleaned_data['mensaje']
                )
                mensaje.save()
            else:
                mensaje = MensajeContacto(
                    usuario_registrado=self.request.user,
                    nombre_de_contacto=self.request.user.username,
                    correo_electronico=self.request.user.username,
                    telefono_de_contacto='',
                    mensaje=form.cleaned_data['mensaje']
                )
                mensaje.save()
            messages.success(self.request,
                             'Tu mensaje ha sido enviado con exito, nos pondremos en contacto contigo proximamente')
            return super().form_valid(form)
        else:
            messages.error(self.request,
                           'No pudimos guardar tu mensaje debido a un error interno, por favor intenta de nuevo')
        return super().form_invalid(form)

