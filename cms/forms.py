from django.contrib.auth.models import User
from django import forms
from .models import MensajeContacto


class MansajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = (
            'nombre_de_contacto',
            'correo_electronico',
            'telefono_de_contacto',
            'mensaje'
        )

        labels = {
            'telefono_de_contacto': 'Telefono de contacto (Opcional):',
            'nombre_de_contacto': 'Nombre de contacto (Opcional):'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_de_contacto'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['correo_electronico'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['telefono_de_contacto'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['mensaje'].widget.attrs.update({
            'class': 'form-control'
        })
