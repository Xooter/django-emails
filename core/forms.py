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


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
