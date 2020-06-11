from django import forms

class AgregaProductoForm(forms.Form):
    pk_producto = forms.IntegerField()
    cantidad = forms.IntegerField()


class BorraProductoEnCarroForm(forms.Form):
    pk_producto = forms.IntegerField()
