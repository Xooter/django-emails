from django import forms
from .models import Lista, Contacto
from django.contrib.auth.models import User

class ListaForm(forms.ModelForm):
    class Meta:
        model = Lista
        fields = ['nombre']

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['email', 'lista']


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=200, label='Asunto')
    body = forms.CharField(widget=forms.Textarea, label='Cuerpo')
