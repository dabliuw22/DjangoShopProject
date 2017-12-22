# -*- coding: utf-8 -*-
from django import forms
from shop import models

class CarritoForm(forms.Form):
    CANTIDAD_CHOICE = [(i,str(i)) for i in range(1, 20)]
    cantidad = forms.IntegerField(label= "Cantidad", initial = 1)
    update_cantidad = forms.BooleanField(required = False, initial = False, widget = forms.HiddenInput)

class OrdenForm(forms.ModelForm):

    class Meta:
        model = models.Orden

        fields = (
            'ciudad',
            'direccion',
        )

        labels = {
            'ciudad': 'Ciudad',
            'direccion': 'Dirección'
        }