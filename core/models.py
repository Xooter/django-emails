from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import validate_email

class Lista(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    email = models.EmailField(validators=[validate_email])
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='contactos')

    def __str__(self):
        return self.email

class EnvioCorreo(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='envios')
    asunto = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enviado a {self.lista.nombre} el {self.fecha_envio}"
