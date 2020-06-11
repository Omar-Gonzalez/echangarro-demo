from .models import Orden, DireccionOrden, ProductoEnOrden


class GuardaOrdenMixin(object):
    def save_orden(self, direccion, carro, estado):
        if estado == 'TENTATIVA':
            try:
                # checa si ya hay una orden tentativa en record, solo puede haber una por cliente en record!
                ordenes_tentativas = Orden.objects.filter(user=self.request.user, estado='TENTATIVA')
                print(ordenes_tentativas.count())
                if ordenes_tentativas.count() > 0:
                    self._update_orden_tentativa(ordenes_tentativas[0], carro, direccion)
                    return
            except:
                # No hay ordenes tenativas procede a crear una
                pass

        orden = Orden(
            user=self.request.user,
            estado=estado
        )
        orden.save()
        direccion_envio = DireccionOrden(
            orden=orden,
            direccion=direccion.direccion,
            colonia=direccion.colonia,
            municipio=direccion.municipio,
            codigo_postal=direccion.codigo_postal,
            estado=direccion.estado,
            referencias=direccion.referencias
        )
        direccion_envio.save()
        for producto in carro.productos:
            p_orden = ProductoEnOrden(
                orden=orden,
                producto=producto.producto,
                cantidad=producto.cantidad
            )
            p_orden.save()

    def _update_orden_tentativa(self, orden_tentativa, carro, direccion):
        for producto in orden_tentativa.productos:
            producto.delete()
        for producto in carro.productos:
            p_orden = ProductoEnOrden(
                orden=orden_tentativa,
                producto=producto.producto,
                cantidad=producto.cantidad
            )
            p_orden.save()
        direccion_u = DireccionOrden.objects.get(orden=orden_tentativa)
        direccion_u.direccion = direccion.direccion
        direccion_u.colonia = direccion.colonia
        direccion_u.municipio = direccion.municipio
        direccion_u.codigo_postal = direccion.codigo_postal
        direccion_u.referencias = direccion.referencias
        direccion_u.save()
        return
