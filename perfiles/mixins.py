from ordenes.models import Orden
from perfiles.models import Direccion, Perfil
from django.contrib import messages
from echangarro.globals import PERFIL_INCOMPLETO
from django.utils.safestring import mark_safe
from .models import ProductoDeseado


class PerfilCompletoMixin(object):
    def verifica_perfil(self):
        # Si el usuario no a completado su perfil levanta warning
        if self.request.user.is_authenticated:
            try:
                perfil = Perfil.objects.get(user=self.request.user)
            except Perfil.DoesNotExist:
                perfil = Perfil(user=self.request.user)
                perfil.save()
            if not perfil.completo:
                messages.warning(self.request, mark_safe(PERFIL_INCOMPLETO))


class PerfilMixin(object):
    def get_perfil_data(self, context):
        perfil = None
        productos_deseados = None
        ordenes = None
        if self.request.user.is_authenticated:
            perfil = Perfil.objects.get(user=self.request.user)
            try:
                productos_deseados = ProductoDeseado.objects.filter(user=self.request.user).all()
                ordenes = Orden.objects.filter(user=self.request.user).exclude(estado='TENTATIVA')
            except ProductoDeseado.DoesNotExist:
                productos_deseados = []
                ordenes = []
            
        context.update({
            'perfil': perfil,
            'ordenes': ordenes,
            'direcciones': Direccion.objects.filter(perfil=perfil),
            'productos_deseados': productos_deseados
        })
        return context
