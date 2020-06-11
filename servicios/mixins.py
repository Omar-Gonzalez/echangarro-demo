from django.contrib import messages
from servicios.models import ServiciosDisponibles


class ServiciosDisponiblesMixin(object):

    @property
    def inventario_desabilitado(self):
        servicios = ServiciosDisponibles.objects.last()
        if servicios == None:
            return False
        if servicios.inventario_disponible == False:
            messages.error(self.request,
                           'EL inventario de este sitio ha sido desabilitado temporalmente, no es necesario notificar al administrador.')
            return True
        else:
            return False

    @property
    def perfil_desabilitado(self):
        servicios = ServiciosDisponibles.objects.last()
        if servicios == None:
            return False
        if servicios.perfil_disponible == False:
            messages.error(self.request,
                           'El sistema de perfiles de la aplicacion esta deesabilitado temporalmente, no es necesario notifcar al adminstrador.')
            return True
        else:
            return False

    @property
    def ordenes_desabilitado(self):
        servicios = ServiciosDisponibles.objects.last()
        if servicios == None:
            return False
        if servicios.ordenes == False:
            messages.error(self.request,
                           'La habilidad de realizar una orden esta suspendida termporalmente, no es necesario notifcar al adminstrador.')
            return True
        else:
            return False
