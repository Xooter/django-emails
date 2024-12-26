from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Lista, Contacto
from django.core.mail import send_mass_mail
from .forms import ListaForm, ContactoForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


def enter(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def quit(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


@login_required
def dashboard(request):
    listas = Lista.objects.filter(usuario=request.user)
    return render(request, 'dashboard.html', {'listas': listas})


@login_required
def new_list(request):
    if request.method == 'POST':
        nombre_lista = request.POST.get('nombre_lista', '')
        correos_string = request.POST.get('emails_hidden', '')
        
        if not nombre_lista:
            return render(request, 'new_list.html', {'error_message': 'El nombre de la lista no puede estar vacío.'})

        correos = [email.strip() for email in correos_string.split(',') if email.strip()]
        if not correos:
            return render(request, 'new_list.html', {'error_message': 'Por lo menos un correo debe ser ingresado.'})

        valid_emails = []
        error_message = None
        for email in correos:
            try:
                validate_email(email)
                valid_emails.append(email)
            except ValidationError:
                error_message = f"El correo {email} no es válido."
                break

        if not error_message:
            lista = Lista.objects.create(nombre=nombre_lista, usuario=request.user)

            for email in valid_emails:
                Contacto.objects.create(email=email, lista=lista)

            success_message = "Lista y contactos creados con éxito"
            return redirect('dashboard')  

        return render(request, 'new_list.html', {'error_message': error_message})

    return render(request, 'new_list.html')


@login_required
def delete_list(request, list_id):
    lista = get_object_or_404(Lista, id=list_id, usuario=request.user)
    
    if request.method == 'POST':
        lista.delete()
        return redirect('dashboard')  
    return redirect('dashboard')  


@login_required
def view_list(request, list_id):
    lista = get_object_or_404(Lista, id=list_id, usuario=request.user)
    contactos = lista.contactos.all()
    return render(request, 'view_list.html', {'lista': lista, 'contactos': contactos})
