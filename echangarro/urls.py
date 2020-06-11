"""echangarro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from productos.views import ProductosListView, ProductoDetalleListView
from perfiles.views import EntraFormView, UsuarioNuevoFormView, cierra_sesion, PerfilUsuarioTemplateView, \
    DireccionUpdateView, PerfilInfoUpdateView, DireccionDeleteView, DireccionCreateView, AddProductoDeseadoFormView, \
    RemueveProductoDeseadoFormView, FotoPerfilFormView, confirma_correo_de_usuario, GeneraPwdFormView, NuevoPwdFormView, \
    CambioDePwdFormView
from carros.views import CarroView, AgregaCarroFormView, ActualizaCarroFormView, BorraProductoEnCarro, CarroAjaxView
from ordenes.views import PreparaOrdenView, ConfirmaDatosView
from cms.views import TerminosTemplateView, PrivacidadTemplateView, ContactoTemplateFormView, \
    Error404TemplateView, Error403TemplateView
from imagenes.views import ImgDetalleTemplateView

admin.site.site_header = 'e-changarro tienda digital'

handler404 = Error404TemplateView.as_view()
handler403 = Error403TemplateView.as_view()
handler500 = 'cms.views.error500'

urlpatterns = [
    path('', ProductosListView.as_view(), name='tienda'),
    path('ofertas/', ProductosListView.as_view(), name='ofertas'),
    path('marcas/', ProductosListView.as_view(), name='marcas'),
    path('categorias/', ProductosListView.as_view(), name='categorias'),
    path('escalas/', ProductosListView.as_view(), name='escalas'),
    path('marca/<str:marca>/', ProductosListView.as_view(), name='marca'),
    path('categoria/<str:categoria>/', ProductosListView.as_view(), name='categoria'),
    path('escala/<str:escala>/', ProductosListView.as_view(), name='escala'),
    path('busqueda/<str:busqueda>/', ProductosListView.as_view(), name='busqueda'),
    path('producto/<str:producto>/', ProductoDetalleListView.as_view(), name='producto'),
    # usuario - profiles
    path('cierra-sesion/', cierra_sesion, name='cierra-sesion'),
    path('entra/', EntraFormView.as_view(), name='entra'),
    path('usuario-nuevo/', UsuarioNuevoFormView.as_view(), name='usuario-nuevo'),
    # carros
    path('carro/', CarroView.as_view(), name='carro'),
    path('carro/agrega-producto/', AgregaCarroFormView.as_view(), name='agrega-producto'),
    path('carro/actualiza-producto/', ActualizaCarroFormView.as_view(), name='actualiza-producto'),
    path('carro/borra-producto/', BorraProductoEnCarro.as_view(), name='borra-producto'),
    # Checkout
    path('carro/prepara-orden/', PreparaOrdenView.as_view(), name='prepara-orden'),
    path('carro/confirma-datos/', ConfirmaDatosView.as_view(), name='confirma-datos'),
    # perfil de usuarios
    path('perfil/', PerfilUsuarioTemplateView.as_view(), name='perfil'),
    path('perfil/direccion/', DireccionCreateView.as_view(), name='direccion'),
    path('perfil/direccion/<int:pk>/', DireccionUpdateView.as_view(), name='direccion-edita'),
    path('perfil/direccion/borra/<int:pk>/', DireccionDeleteView.as_view(), name='direccion-borra'),
    path('perfil/info/<int:pk>/', PerfilInfoUpdateView.as_view(), name='perfil-edita'),
    path('perfil/producto-deseado/', AddProductoDeseadoFormView.as_view(), name='lista-deseado'),
    path('perfil/remueve-producto-deseado/', RemueveProductoDeseadoFormView.as_view(), name='remueve-deseado'),
    path('perfil/foto/', FotoPerfilFormView.as_view(), name='cambia-foto-perfil'),
    path('perfil/confirma-correo/<str:uuid>/', confirma_correo_de_usuario),
    path('perfil/genera-pwd/', GeneraPwdFormView.as_view(), name='genera-pwd'),
    path('perfil/nuevo-pwd/<str:uuid>/', NuevoPwdFormView.as_view(), name='nuevo-pwd'),
    path('perfil/cambia-pwd/', CambioDePwdFormView.as_view(), name='cambia-pwd'),
    # recursos / ajax
    path('recursos/imagen/<int:prod_pk>/<int:img_pk>/', ImgDetalleTemplateView.as_view(), name='imagen-detalle'),
    path('recursos/carrito/', CarroAjaxView.as_view(), name='ajax-carrito'),
    # paginas info
    path('terminos-y-condiciones/', TerminosTemplateView.as_view(), name='terminos'),
    path('aviso-de-privacidad/', PrivacidadTemplateView.as_view(), name='privacidad'),
    path('contacto/', ContactoTemplateFormView.as_view(), name='contacto'),
    # robots.txt
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /admin/", content_type="text/plain")),
    # admin
    path('admin/', admin.site.urls),
]