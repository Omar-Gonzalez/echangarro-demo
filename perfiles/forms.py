from django.contrib.auth.models import User
from django import forms
from perfiles.models import Direccion, Perfil


class EntraForm(forms.Form):
    email = forms.CharField(label='Correo de cuenta', max_length=150)
    contraseña = forms.CharField(widget=forms.PasswordInput())

    email.widget.attrs.update({
        'class': 'form-control'
    })

    contraseña.widget.attrs.update({
        'class': 'form-control'
    })


class UsuarioNuevoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError('Tu password debe contener al menos 6 caracteres de largo')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            existe = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('Este coreo ya esta en uso, por favor intenta de nuevo con otra direccion')

    def save(self, commit=True):
        user = super(UsuarioNuevoForm, self).save(commit=False)

        email = self.data['email']
        email = (email[:150]) if len(email) > 150 else email
        user.username = email
        user.set_password(self.data["password"])

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = (
            'direccion',
            'colonia',
            'municipio',
            'codigo_postal',
            'estado',
            'referencias'
        )
        labels = {
            'direccion': 'Calle con numero exterior o interior',
            'referencias': 'Referencias (opcional):'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['colonia'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['municipio'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['codigo_postal'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['referencias'].widget.attrs.update({
            'class': 'form-control'
        })


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = (
            'nombre',
            'apeidos',
            'telefono',
            'telefono_alternativo'
        )
        labels = {
            'telefono': 'Telefono de contacto',
            'telefono_alternativo': 'Telefono alternativo (opcional)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['apeidos'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['telefono_alternativo'].widget.attrs.update({
            'class': 'form-control'
        })


class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = (
            'foto_de_perfil',
        )

        labels = {
            'foto_de_perfil': 'Cambia tu foto de perfil'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto_de_perfil'].widget.attrs.update({
            'class': 'form-control'
        })


class ProductoDeseadoForm(forms.Form):
    pk_producto = forms.IntegerField()
    next = forms.CharField()


class RemueveProdDeseadoForm(forms.Form):
    pk_producto = forms.IntegerField()


class GeneraPwdForm(forms.Form):
    correo_de_cuenta = forms.EmailField()

    correo_de_cuenta.widget.attrs.update({
        'class': 'form-control'
    })


class NuevPwdForm(forms.Form):
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput())
    verifica_contraseña = forms.CharField(widget=forms.PasswordInput())

    nueva_contraseña.widget.attrs.update({
        'class': 'form-control'
    })

    verifica_contraseña.widget.attrs.update({
        'class': 'form-control'
    })
