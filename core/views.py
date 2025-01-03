from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Lista, Contacto ,EnvioCorreo
from django.core.mail import send_mail
from .forms import ListaForm, ContactoForm,EmailForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse

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
    lista = get_object_or_404(Lista, id=list_id)
    contactos = lista.contactos.all()

    ultimo_envio = lista.envios.last()

    return render(request, 'view_list.html', {
        'lista': lista,
        'contactos': contactos,
        'ultimo_envio': ultimo_envio
    })


@login_required
def send_mails(request, list_id):
    lista = get_object_or_404(Lista, id=list_id)
    contactos = lista.contactos.all()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            emails = [contacto.email for contacto in contactos]

            send_mail(subject, body, 'joaquinrighetti@gmail.com', emails)

            EnvioCorreo.objects.create(
                lista=lista,
                asunto=subject,
                cuerpo=body
            )

            messages.success(request, "Los correos se han enviado correctamente.")

            return redirect('view_list', list_id=lista.id)

    else:
        form = EmailForm()

    return render(request, 'view_list.html', {
        'form': form, 
        'lista': lista, 
        'contactos': contactos
    })
