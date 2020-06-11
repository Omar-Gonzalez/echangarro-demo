from django import forms
from echangarro.globals import PREFERENCIA_PAGO_CHOICES


class SelDireccionForm(forms.Form):

    def __init__(self, direcciones, *args, **kwargs):
        super(SelDireccionForm, self).__init__(*args, **kwargs)

        direccion_choices = list()
        for direccion in direcciones:
            direccion_choices.append((direccion.pk, direccion))

        self.fields['direccion_de_envio'] = forms.ChoiceField(choices=direccion_choices)
        self.fields['direccion_de_envio'].label = 'Selecciona direccion de envio'

        self.fields['direccion_de_envio'].widget.attrs.update({
            'class': 'form-control'
        })

class ConfirmaOrdenForm(forms.Form):
    confirmacion = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    preferencia_de_pago = forms.ChoiceField(choices=PREFERENCIA_PAGO_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferencia_de_pago'].widget.attrs.update({
            'class': 'form-control'
        })
