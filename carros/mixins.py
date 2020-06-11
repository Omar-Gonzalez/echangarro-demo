from carros.models import Carro


class CarroDeUsuarioMixin(object):

    def get_carro_data(self, context):
        carro = Carro.objects.filter(user=self.request.user.id).first()
        context.update({
            'carro': carro,
        })
        return context

    @property
    def carro(self):
        carro = Carro.objects.filter(user=self.request.user.id).first()
        return carro
