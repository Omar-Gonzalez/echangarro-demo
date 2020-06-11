from .models import Configuracion


class ConfigMixin(object):
    def get_config_data(self, context):
        config = Configuracion.objects.last()
        context.update({
            'config': config
        })
        return context
