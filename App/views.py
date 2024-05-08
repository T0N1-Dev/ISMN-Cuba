import base64
import json
import os
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from random import randint
from smtplib import SMTPServerDisconnected, SMTPAuthenticationError

import bs4
import requests
from PIL import Image as PILImage
from barcode import EAN13
from barcode.writer import ImageWriter
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pathlib import Path

from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets import signsandsymbols

from App.forms import ChangePasswordForm
from App.models import (Editor, Musical_Publication, Registered_Data, PrefijoEditor, PrefijoPublicacion,
                        Rango_Prefijo_Editor, Rango_Prefijo_Publicacion, Solicitud)
from django.views.decorators.cache import cache_control
from django.contrib import messages  # Return messages
from django.http import HttpResponseRedirect, JsonResponse  # Redirect the page after submit
from django.db.models import Q, Max, Count
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives  # Required to send emails
from django.template import loader  # Render templates on email body
from django.contrib.auth.views import LoginView, LogoutView
import io
from django.http import FileResponse
# REPORTLAB
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image, Frame, PageTemplate, PageBreak
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, letter, landscape

# ================= VARIABLES TEMPORALES =================
from djangoProject.settings import MEDIA_ROOT, BASE_DIR


# ================= SECCIÓN DE SEGURIDAD Y AUTENTICACIÓN =================
class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return '/admin/'
        else:
            return reverse('frontend')


class MyLogoutView(LogoutView):
    next_page = '/'


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f"Se ha cambiado su contraseña exitosamente.")
            return HttpResponseRedirect('/')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'registration/change_password.html', {"form": form})


# ================= SECCIÓN DE CREACIÓN DE RANGOS Y PREFIJOS =================
def generate_prefijo_editor(range):
    value = 0
    lote = '979-0'
    if range == 'p-menor':
        max_menor = PrefijoEditor.objects.filter(rango__tipo='P-Menor').aggregate(Max('value'))['value__max']
        if max_menor:
            value = max_menor + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Menor'))
        else:
            return PrefijoEditor.objects.create(value=100001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Menor'))
    elif range == 'p-inferior':
        max_inferior = PrefijoEditor.objects.filter(rango__tipo='P-Inferior').aggregate(Max('value'))['value__max']
        if max_inferior:
            value = max_inferior + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Inferior'))
        else:
            return PrefijoEditor.objects.create(value=10001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Inferior'))
    elif range == 'p-medio_inferior':
        max_medio_inf = PrefijoEditor.objects.filter(rango__tipo='P-Medio_Inferior').aggregate(Max('value'))[
            'value__max']
        if max_medio_inf:
            value = max_medio_inf + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio_Inferior'))
        else:
            return PrefijoEditor.objects.create(value=1001, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio_Inferior'))
    elif range == 'p-medio':
        max_medio = PrefijoEditor.objects.filter(rango__tipo='P-Medio').aggregate(Max('value'))['value__max']
        if max_medio:
            value = max_medio + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio'))
        else:
            return PrefijoEditor.objects.create(value=101, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Medio'))
    elif range == 'p-superior':
        max_superior = PrefijoEditor.objects.filter(rango__tipo='P-Superior').aggregate(Max('value'))['value__max']
        if max_superior:
            value = max_superior + 1
            return PrefijoEditor.objects.create(value=value, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Superior'))
        else:
            return PrefijoEditor.objects.create(value=1, lote=lote,
                                                rango=Rango_Prefijo_Editor.objects.get(tipo='P-Superior'))


def generate_prefijo_publicacion(valor):
    if valor.__len__() == 2:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(tipo='P-Menor'))
        return prefijo
    elif valor.__len__() == 3:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Inferior'))
        return prefijo
    elif valor.__len__() == 4:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Media_Inferior'))
        return prefijo
    elif valor.__len__() == 5:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(tipo='P-Media'))
        return prefijo
    else:
        prefijo = PrefijoPublicacion.objects.create(value=valor, lote='979-0',
                                                    rango=Rango_Prefijo_Publicacion.objects.get(
                                                        tipo='P-Superior'))
        return prefijo


# Registration Function
def register_user(request):
    if request.method == 'POST':
        # Check if email exists in BD
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        id_tribute = request.POST['idTribute']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Este teléfono ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        elif Registered_Data.objects.filter(user_name=username).exists():
            messages.error(request, "Este nombre de usuario ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        elif Registered_Data.objects.filter(id_tribute=id_tribute).exists():
            messages.error(request, "Esta identificación tributaria ya ha sido registrada en nuestra Base de Datos")
            return HttpResponseRedirect('/login')
        # ===========================
        else:
            if request.POST.get('username') \
                    and request.POST.get('first_name') \
                    and request.POST.get('password') \
                    and request.POST.get('phone') \
                    and request.POST.get('email') \
                    and request.POST.get('editorType') \
                    and request.POST.get('address') \
                    and request.POST.get('idTribute') \
                    and request.POST.get('editorPrefijo'):
                datos = request.POST.copy()
                if request.FILES:
                    # Convertir la imagen a base64 para poder serializarla a JSON en el request.session
                    datos['imagenProfile'] = base64.b64encode(request.FILES['imagenProfile'].read())
                    # Agregar la informacion inicial para que pueda ser leida por el "src" de <img> en el html
                    imagen_extension = request.FILES['imagenProfile'].content_type
                    datos['imagenProfile'] = f"data:{imagen_extension};base64," + datos['imagenProfile']
                else:
                    with open(f"{MEDIA_ROOT}\profile_default.png", "rb") as image_profile:
                        datos['imagenProfile'] = f"data:png;base64," + base64.b64encode(image_profile.read()).decode()
                        image_profile.close()

                confirmation_code = send_code_confirmation(request)
                datos['code_confirmation'] = confirmation_code
                request.session['datos'] = datos
                return render(request, 'registration/email_confirmation.html')
            else:
                messages.error(request, "Complete todos los campos del formulario")
                return HttpResponseRedirect('/register_user')
    else:
        return render(request, 'registration/register_user.html')


def email_confirmation(request):
    if request.method == 'POST':
        if request.POST.get('code') != str(request.session.get('datos')['code_confirmation']):
            messages.error(request, 'Código incorrecto. Revise su correo electrónico')
            return HttpResponseRedirect('/email_confirmation')
        else:
            solicitud = Solicitud()
            solicitud.tipo = 'Solicitud-Inscripción'
            solicitud.status = 'Pendiente'
            solicitud.temporal = request.session.get('datos')
            solicitud.save()
            messages.success(request, 'Su solicitud se ha enviado correctamente, le notificaremos a su correo '
                                      'cuando haya sido aceptada.')
            return HttpResponseRedirect('/')
    else:
        return render(request, 'registration/email_confirmation.html')


# ================= SECCIÓN DEL USUARIO (EDITOR) =================
# Function to render the Home Page for everybody
def frontend(request):
    return render(request, 'frontend.html')


# ================= SECCIÓN DEL USUARIO (ESPECIALISTA) =================
# Function to render editor's lists
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_editores(request, order):
    if request.POST:
        return export_editores_list(request)
    else:
        if 'q' in request.GET:
            flag = 'list_dsc'
            q = request.GET['q']
            all_editor_list = Editor.objects.filter(
                Q(user__username__icontains=q) | Q(user__email__icontains=q) | Q(directions__icontains=q) |
                Q(note__icontains=q) | Q(user__first_name__icontains=q) | Q(type__icontains=q)
            ).order_by('-user__date_joined')
            if q.isnumeric():
                all_editor_list = Editor.objects.filter(Q(phone__contains=q) | Q(prefijo__value__contains=q) |
                                                        Q(id_tribute=q)).order_by('-user__date_joined')
        elif order == 'list_dsc':
            all_editor_list = Editor.objects.all()[::-1]
            # Para ordenar ascendente o descendente
            flag = 'list_asc'
        else:
            all_editor_list = Editor.objects.all()
            flag = 'list_dsc'

        paginator = Paginator(all_editor_list, 5)
        page = request.GET.get('page')
        all_editor = paginator.get_page(page)
        solicitudes_pendientes = Solicitud.filter_pending_not_deleted_ordered()
        usuario = request.user
        return render(request, 'editores/editores-list.html', {"editores": all_editor,
                                                               'solicitudes_pendientes': solicitudes_pendientes,
                                                               'usuario': usuario, 'flag': flag})

# Function to render publication's lists
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_publicaciones(request, order):
    if request.POST:
        return export_publications_list(request)
    else:
        if 'q' in request.GET:
            flag = 'list_dsc'
            q = request.GET['q']
            all_publication_list = Musical_Publication.objects.filter(
                Q(name__icontains=q) | Q(autor__icontains=q) | Q(editor__user__username__icontains=q) |
                Q(gender__icontains=q) | Q(ismn__icontains=q)
            ).order_by('-created_at')
        elif order == 'list_dsc':
            all_publication_list = Musical_Publication.objects.all().order_by('-created_at')
            # Para ordenar ascendente o descendente
            flag = 'list_asc'
        else:
            all_publication_list = Musical_Publication.objects.all()
            flag = 'list_dsc'

        paginator = Paginator(all_publication_list, 5)
        page = request.GET.get('page')
        all_publication = paginator.get_page(page)
        solicitudes_pendientes = Solicitud.filter_pending_not_deleted_ordered()
        return render(request, 'publicaciones/publications-list.html', {"publicaciones": all_publication,
                                                                        'solicitudes_pendientes': solicitudes_pendientes,
                                                                        'flag': flag})


# Function to render las listas de solicitudes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_solicitudes(request, order):
    if request.method == "POST":
        return export_solicitudes_list(request)
    else:
        if 'q' in request.GET:
            flag = 'list_dsc'
            q = request.GET['q']
            all_solicitudes_list = Solicitud.objects.filter(
                Q(tipo__icontains=q) | Q(editor__user__username__icontains=q) |
                Q(status__icontains=q, deleted=False)
            ).order_by('-created_at')
        elif order == 'list_dsc':
            all_solicitudes_list = Solicitud.objects.filter(deleted=False).order_by('-created_at')
            # Para ordenar ascendente o descendente
            flag = 'list_asc'
        else:
            all_solicitudes_list = Solicitud.objects.filter(deleted=False)
            flag = 'list_dsc'

        paginator = Paginator(all_solicitudes_list, 5)
        page = request.GET.get('page')
        all_solicitudes = paginator.get_page(page)
        solicitudes_pendientes = Solicitud.filter_pending_not_deleted_ordered()
        solicitudes_rechazadas = Solicitud.return_deleted()
        solicitudes_enviadas = Solicitud.solicitudes_enviadas_total()
        # Solo me interesan las últimas 30 que representan un mes
        solicitudes_aceptadas = dict(list(Solicitud.return_accepted().items())[-31:])
        return render(request, 'solicitudes/solicitudes-list.html', {"solicitudes": all_solicitudes, 'flag': flag,
                                                                     "solicitudes_pendientes": solicitudes_pendientes,
                                                                     "solicitudes_rechazadas": solicitudes_rechazadas,
                                                                     "solicitudes_enviadas": solicitudes_enviadas,
                                                                     "solicitudes_aceptadas": solicitudes_aceptadas})


def guardar_imagen_base64(base64_string, name):
    # Extraer el base64 y la extension de la imagen
    header, base64_data = base64_string.split(';base64,')

    if 'jpg' in header or 'jpeg' in header:
        extension = header.split('/')[-1]
    elif 'png' in header:
        extension = header.split(':')[-1]
    else:
        return ''

    # Decodificar la cadena base64 en una imagen
    image_data = base64.b64decode(base64_data)

    # Crear una imagen PIL desde los datos decodificados
    image = PILImage.open(io.BytesIO(image_data))
    # Crear un InMemoryUploadedFile a partir de la imagen PIL
    image_io = io.BytesIO()
    image.save(image_io, format=extension.upper())
    image_file = InMemoryUploadedFile(image_io, None, f'{name}_image.{extension}',
                                      f'image/{extension}', image_io.tell(), None)
    return image_file


# Function to Accept an Inscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def accept_inscription(request, solicitud_id):
    solicitud = Solicitud.objects.get(id=solicitud_id)
    prefijo_editor = generate_prefijo_editor(solicitud.temporal['editorPrefijo'])
    user = User()
    editor = Editor()
    user.username = solicitud.temporal['username']
    user.set_password(solicitud.temporal['password'])
    user.first_name = solicitud.temporal['first_name']
    user.email = solicitud.temporal['email']
    if solicitud.temporal['editorType'] == 'Independiente':
        user.last_name = solicitud.temporal['last_name']
        editor.birthday = solicitud.temporal['birthday']
    editor.user = user
    editor.phone = solicitud.temporal['phone']
    editor.prefijo = prefijo_editor
    editor.type = solicitud.temporal['editorType']
    # PARA TRANSFORMAR DE BASE64 A IMAGE
    imagen = guardar_imagen_base64(solicitud.temporal['imagenProfile'], user.first_name)
    editor.image_profile = imagen
    editor.note = solicitud.temporal['note']
    editor.directions = solicitud.temporal['address']
    editor.id_tribute = solicitud.temporal['idTribute']
    solicitud.editor = editor
    solicitud.status = 'Atendido'
    contact = Registered_Data()
    contact.email = user.email
    contact.phone = editor.phone
    contact.user_name = user.username
    correo = send_info_inscripcion(nombre=user.first_name, user_email=user.email,
                                   username=user.username, password=solicitud.temporal['password'])
    solicitud.temporal = {}
    if correo:
        user.save()
        editor.save()
        solicitud.save()
        contact.save()
        messages.success(request,
                         f"Se ha aceptado la solicitud de inscripción y se ha notificado a {user.first_name} a "
                         f"su correo. Ahora {user.first_name} ya "
                         f"puede realizar solicitudes ISMN !")

    else:
        messages.error(request, 'Ha ocurrido un error al intentar notificar al correo del cliente, pruebe más tarde')
    return HttpResponseRedirect('/backend_solicitudes/list_dsc')


# Reformat the path to files since their names
def reformat_path(path, ruta_pathlib):
    part_path = path.split('/')[2:]  # Extrayendo /temp/nombre_del_file.extension
    return Path(ruta_pathlib, part_path[0], part_path[1])


# Function to Accept an Inscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def accept_ismn_solicitud(request, solicitud_id):
    # Variables
    solicitud = Solicitud.objects.get(id=solicitud_id)
    publicacion = Musical_Publication()
    prefijo_str_publicacion = solicitud.temporal['ismn'].split('-')[3]
    publicacion_prefijo = generate_prefijo_publicacion(prefijo_str_publicacion)
    ruta_letra_publicacion = reformat_path(solicitud.temporal['publication_letra'], MEDIA_ROOT)
    if solicitud.temporal['publication_image']:
        ruta_imagen_publicacion = reformat_path(solicitud.temporal['publication_image'], MEDIA_ROOT)
    else:
        ruta_imagen_publicacion = Path(f'{MEDIA_ROOT}\default.jpg')

    # Asignacion y salvas
    publicacion.name = solicitud.temporal['title']
    publicacion.autor = solicitud.temporal['autor']
    publicacion.editor = solicitud.editor
    publicacion.prefijo = publicacion_prefijo
    publicacion.ismn = solicitud.temporal['ismn']
    barcode_rute, barcode_io = generate_barcode(publicacion.ismn, publicacion.name)
    publicacion.description = solicitud.temporal['note']
    publicacion.date_time = datetime.strptime(solicitud.temporal['date'], '%Y-%m-%d')
    publicacion.gender = solicitud.temporal['gender']
    with open(ruta_letra_publicacion, 'rb') as letra_file:
        publicacion.letra.save(f'{ruta_letra_publicacion.stem}.{ruta_letra_publicacion.suffix}',
                               File(letra_file), save=True)
        letra_file.close()

    if solicitud.temporal['publication_image']:
        with open(ruta_imagen_publicacion, 'rb') as image_file:
            publicacion.imagen.save(f'{ruta_imagen_publicacion.stem}.{ruta_imagen_publicacion.suffix}',
                                    File(image_file), save=True)
            image_file.close()
    publicacion.barcode.save(f'{barcode_rute.stem}{barcode_rute.suffix}', File(barcode_io), save=True)
    # Enviar email de aceptacion
    email_send = send_solicitud_ismn_accepted(request.user, publicacion)
    if email_send:
        solicitud.status = 'Atendido'
        # Eliminando datos temporales
        if solicitud.temporal['publication_image']:
            os.remove(f"{BASE_DIR}\{solicitud.temporal['publication_image']}")
        os.remove(f"{BASE_DIR}\{solicitud.temporal['publication_letra']}")
        del solicitud.temporal['publication_image']
        del solicitud.temporal['csrfmiddlewaretoken']
        publicacion.save()
        solicitud.save()
        messages.success(request, f"Se ha aceptado la solicitud ISMN y se ha notificado a {solicitud.editor} a "
                                  f"su correo.")
        return HttpResponseRedirect('/backend_solicitudes/list_dsc')
    else:
        messages.error(request,
                       "Ha ocurrido un error al intentar notificar al correo del editor. Por favor contactelo.")
        return HttpResponseRedirect('/backend_solicitudes/list_dsc')


# Function to Add Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_editor(request):
    if request.method == 'POST':
        # Check if email exist in BD
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        id_tribute = request.POST['idTribute']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/add_editor')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Este teléfono ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/add_editor')
        elif Registered_Data.objects.filter(user_name=username).exists():
            messages.error(request, "Este nombre de usuario ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/add_editor')
        elif Registered_Data.objects.filter(id_tribute=id_tribute).exists():
            messages.error(request, "Esta identificación tributaria ya ha sido registrada en nuestra Base de Datos")
            return HttpResponseRedirect('/add_editor')
        # ===========================
        else:
            if request.POST.get('username') \
                    and request.POST.get('first_name') \
                    and request.POST.get('password') \
                    and request.POST.get('phone') \
                    and request.POST.get('email') \
                    and request.POST.get('editorType') \
                    and request.POST.get('address') \
                    and request.POST.get('idTribute') \
                    and request.POST.get('editorPrefijo'):
                editor = Editor()
                user = User()
                user.username = request.POST.get('username')
                user.set_password(request.POST.get('password'))
                user.first_name = request.POST.get('first_name')
                editor.phone = request.POST.get('phone')
                user.email = request.POST.get('email')
                editor.directions = request.POST.get('address')
                editor.type = request.POST.get('editorType')
                if editor.type == 'Independiente':
                    user.last_name = request.POST.get('last_name')
                    editor.birthday = request.POST.get('birthday')
                editor.directions = request.POST.get('address')
                editor.id_tribute = request.POST.get('idTribute')
                editor.user = user
                editor.prefijo = generate_prefijo_editor(request.POST.get('editorPrefijo'))
                editor.note = request.POST.get('note')
                if request.FILES.get('imagenProfile'):
                    editor.image_profile = request.FILES.get('imagenProfile')
                user.save()
                editor.save()
                # Register email and phone inside BD
                contact = Registered_Data()
                contact.user_name = user.username
                contact.email = email
                contact.phone = phone
                contact.id_tribute = id_tribute
                contact.save()
                # ========================

                messages.success(request, "Editor añadido correctamente !")
                return HttpResponseRedirect('/backend/list_dsc')
    elif request.method == 'GET':
        if Solicitud.objects.filter(status='Pendiente').filter(tipo='Solicitud-Inscripción').exists():
            messages.error(request, 'No es posible añadir un editor en este momento. '
                                    'Atienda las solicitudes de inscripción que han sido enviadas y luego regrese.')
            return HttpResponseRedirect('/backend/list_dsc')
        else:
            return render(request, "editores/add.html")


# Function to delete Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    if editor.image_profile.name != 'profile_default.png':
        editor.image_profile.delete()
    Registered_Data.objects.get(phone=editor.phone).delete()
    User.objects.get(username=editor.user.username).delete()
    editor.delete()
    messages.success(request, "Editor eliminado correctamente !")
    return HttpResponseRedirect('/backend/list_dsc')


# Function to access the Editor individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    solicitud_inscripcion = Solicitud.objects.filter(tipo='Solicitud-Inscripción').filter(status='Pendiente').exists()
    if editor:
        if solicitud_inscripcion:
            messages.error(request, 'No es posible editar un editor en este momento. '
                                    'Atienda las solicitudes de inscripción que han sido enviadas y luego regrese.')
            return HttpResponseRedirect('/backend/list_dsc')
        else:
            return render(request, "editores/edit.html", {"editor": editor})
    else:
        return HttpResponseRedirect('/backend/list_dsc')


# Function to edit the Editor
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_editor(request):
    if request.method == "POST":
        editor = Editor.objects.get(id=request.POST.get('id'))
        if editor:
            editor.user.username = request.POST.get('username')
            editor.user.first_name = request.POST.get('first_name')
            editor.phone = request.POST.get('phone')
            editor.user.email = request.POST.get("email")
            editor.directions = request.POST.get('address')
            editor.type = request.POST.get("editorType")
            if request.POST.get('birthday'):
                editor.birthday = request.POST.get("birthday")
                editor.user.last_name = request.POST.get('last_name')
            editor.id_tribute = request.POST.get("idTribute")
            editor.note = request.POST.get("note")
            editor.image_profile = request.FILES.get('imagenProfile')
            editor.save()
            messages.success(request, "Editor editado correctamente !")
            return HttpResponseRedirect('/backend/list_dsc')


# Function to show musical collections
def musical_colections_list(request):
    Musical_Collections_Objects = Musical_Publication.objects.all().order_by('-created_at')
    data = {
        'publicaciones_musicales': Musical_Collections_Objects,
    }

    if not Musical_Collections_Objects:
        data['mensaje'] = "No hay publicaciones musicales en el sistema"
        return render(request, 'colecciones-musicales.html', data)
    elif 'q' in request.GET:
        q = request.GET['q']
        data['publicaciones_musicales'] = Musical_Publication.objects.filter(
            Q(name__icontains=q) | Q(autor__icontains=q) | Q(gender__icontains=q)
        )
        if not data['publicaciones_musicales']:
            data['mensaje'] = "No hay coincidencias"
    return render(request, 'colecciones-musicales.html', data)


# Function to generate a barcode
def generate_barcode(ismn, titulo):
    ruta = f'{MEDIA_ROOT}\\publications\\barcodes\\{titulo}_barcode'
    number = ismn.replace('-', '')
    bar_code = EAN13(number, writer=ImageWriter())
    bytes_io = io.BytesIO()
    bar_code.write(bytes_io)
    return Path(ruta + '.png'), bytes_io


# Function to add a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_musical_publication(request):
    if request.method == 'POST':
        if request.POST.get('title') \
                and request.POST.get('autor') \
                and request.POST.get('editor') \
                and request.POST.get('prefijo-publicacion') \
                and request.POST.get('ismn') \
                and request.POST.get('gender') \
                and request.POST.get('date'):
            musical_publication = Musical_Publication()
            editor = Editor.objects.get(user__first_name=request.POST.get('editor'))
            prefijo_value = request.POST.get('prefijo-publicacion').rpartition(" ")[2]
            prefijo = generate_prefijo_publicacion(prefijo_value)
            musical_publication.name = request.POST.get('title')
            musical_publication.autor = request.POST.get('autor')
            musical_publication.editor = editor
            musical_publication.prefijo = prefijo
            musical_publication.ismn = request.POST.get('ismn')
            barcode_rute, barcode_io = generate_barcode(musical_publication.ismn, musical_publication.name)
            musical_publication.gender = request.POST.get('gender')
            musical_publication.letra = request.FILES.get('publication_letter')
            if request.FILES.get('publication_image'):
                musical_publication.imagen = request.FILES.get('publication_image')
            else:
                pass
            musical_publication.description = request.POST.get('note')
            musical_publication.date_time = request.POST.get('date')
            musical_publication.barcode.save(f'{barcode_rute.stem}{barcode_rute.suffix}',
                                             File(barcode_io), save=True)
            musical_publication.save()
            messages.success(request, "Publicación musical añadida correctamente !")
            return HttpResponseRedirect('/backend_publicaciones/list_dsc')
    elif request.method == 'GET':
        if Solicitud.objects.filter(status='Pendiente').exists():
            messages.error(request, 'No es posible añadir una publicación en estos momentos. '
                                    'Atienda las solicitudes ISMN que han sido enviadas y luego regrese.')
            return HttpResponseRedirect('/backend_publicaciones/list_dsc')
        else:
            editores = Editor.objects.annotate(Count('musical_publication'))
            data = {'editores': editores}
            return render(request, "publicaciones/add_publication.html", data)


# Function to access the musical_publication individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    editores = Editor.objects.all()
    data = {"musical_publication": musical_publication, "editores": editores}
    if Solicitud.objects.filter(status='Pendiente').filter(tipo='Solicitud-ISMN').exists():
        messages.error(request, 'No es posible editar una publicación en estos momentos. '
                                'Atienda las solicitudes ISMN que han sido enviadas y luego regrese.')
        return HttpResponseRedirect('/backend_publicaciones/list_dsc')
    else:
        return render(request, "publicaciones/edit_publication.html", data)


# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_musical_publication(request):
    if request.method == "POST":
        musical_publication = Musical_Publication.objects.get(id=request.POST.get('id'))
        if musical_publication:
            musical_publication.name = request.POST.get('title')
            musical_publication.autor = request.POST.get('autor')
            if request.POST.get('editor') != str(musical_publication.editor):
                editor = Editor.objects.get(user__first_name=request.POST.get('editor'))
                musical_publication.editor = editor
                prefijo_value = request.POST.get('prefijo-publicacion').rpartition(" ")[2]
                prefijo = generate_prefijo_publicacion(prefijo_value)
                musical_publication.prefijo = prefijo
                musical_publication.ismn = request.POST.get('ismn')
            else:
                pass
            musical_publication.gender = request.POST.get('gender')
            if request.FILES.get('publication_letter'):
                musical_publication.letra = request.FILES.get('publication_letter')
            else:
                pass
            if request.FILES.get('publication_image'):
                musical_publication.imagen = request.FILES.get('publication_image')
            else:
                pass
            musical_publication.description = request.POST.get('note')
            musical_publication.date_time = request.POST.get('date')
            musical_publication.save()
            messages.success(request, "Publicacion Musical actualizada correctamente !")
            return HttpResponseRedirect('/backend_publicaciones/list_dsc')


# Function to delete a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    musical_publication.letra.delete()
    musical_publication.barcode.delete()
    if musical_publication.imagen.name != 'default.jpg':
        musical_publication.imagen.delete()
    musical_publication.prefijo.delete()
    musical_publication.delete()
    messages.success(request, "Publicacion Musical eliminada correctamente !")
    return HttpResponseRedirect('/backend_publicaciones/list_dsc')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_solicitud(request, solicitud_id):
    solicitud = Solicitud.objects.get(id=solicitud_id)
    if solicitud.tipo == 'Solicitud-ISMN':
        if solicitud.temporal['publication_image']:
            os.remove(f"{BASE_DIR}\{solicitud.temporal['publication_image']}")
        try:
            os.remove(f"{BASE_DIR}\{solicitud.temporal['publication_letra']}")
        except FileNotFoundError:
            pass
    solicitud.soft_delete()
    solicitud.save()
    messages.success(request, "Solicitud eliminada correctamente !")
    return HttpResponseRedirect('/backend_solicitudes/list_dsc')


# ---- GENERAR ISMN ------
def generar_ismn(editor):
    """ Notas
        1- La cantidad de digitos que debe tener un ismn en total para Cuba son 13
        2- La cantidad de digitos que deben sumar los prefijos de publicacion y editor son 8
        3- El digito de control se calcula mediante este metodo http://www.grupoalquerque.es/mate_cerca/paneles_2012/168_ISBN2.pdf
    """

    # Funcion que formatea el prefijo_publicacion para que tenga el formato de ismn: 001,012,0002, etc
    def formatear_prefijo(valor, cant_digitos_prefijo_companiero):
        # Cantidad de digitos que debe tener la publicacion segun las reglas ISMN
        cant_digitos = 8 - cant_digitos_prefijo_companiero

        # Cantidad de ceros que debe agregar al prefijo de la publicacion
        cant_zeros = cant_digitos - len(valor)

        # Retorna el valor de la publicacion listo para insertar en el ISMN
        return '0' * cant_zeros + valor

    # Para determinar el valor del prefijo de la publicacion
    def determinar_valor_prefijo_publicacion(musical_pub_exist, solicitud_ismn_exist):
        valor_prefijo_ultima_publicacion = \
            editor.musical_publication_set.aggregate(Max('prefijo__value'))['prefijo__value__max'] \
                if musical_pub_exist else 0
        valor_prefijo_ultima_solicitud = int(
            editor.solicitud_set.filter(deleted=False).last().temporal.get('ismn').split('-')[-2]) if solicitud_ismn_exist else 0
        valor_prefijo_publicacion = max(valor_prefijo_ultima_solicitud, valor_prefijo_ultima_publicacion)
        return valor_prefijo_publicacion + 1

    # Funcion para calcular el digito de control
    def digito_control(editor_prefijo, publicacion_prefijo):
        sum = 39  # Esta es la suma de lote '979-0' aplicando el metodo de 9*1 + 7*3 + 9*1 + 0*3 = 39.
        multiplicador = [1, 3]  # Multiplicadores que se van alternando en cada digito de ambos prefijos
        # (Editor, Publicacion) para crear el digito de control.
        digit_control = int  # Puede tener valor minimo de 0 y maximo de 9.

        for i in range(len(editor_prefijo)):
            if i % 2 == 0:
                sum += int(editor_prefijo[i]) * multiplicador[0]
            else:
                sum += int(editor_prefijo[i]) * multiplicador[1]

        if len(editor_prefijo) % 2 != 0:
            multiplicador = [3, 1]

        for i in range(len(publicacion_prefijo)):
            if i % 2 == 0:
                sum += int(publicacion_prefijo[i]) * multiplicador[0]
            else:
                sum += int(publicacion_prefijo[i]) * multiplicador[1]

        for i in range(10):
            if (sum + i) % 10 == 0:
                digit_control = i
                break

        return str(digit_control)

    # Funcion que conforma el ISMN con sus diferentes partes
    def crear_ismn(editor_prefijo, publicacion_prefijo):
        digit_validation = digito_control(editor_prefijo, publicacion_prefijo)
        return '979-0' + '-' + editor_prefijo + '-' + publicacion_prefijo + '-' + digit_validation

    cant_digitos_prefijo_editor = str(editor.prefijo.rango.rango_superior).__len__()
    valor_prefijo_public = determinar_valor_prefijo_publicacion(editor.musical_publication_set.exists(),
                                                                editor.solicitud_set.filter(
                                                                    tipo='Solicitud-ISMN').filter(
                                                                    status='Pendiente', deleted=False).exists())
    prefijo_publicacion = formatear_prefijo(str(valor_prefijo_public), cant_digitos_prefijo_editor)

    #   En el excepcional caso que el prefijo del editor necesite un cero delante
    if editor.prefijo.value < 10:
        prefijo_editor = formatear_prefijo(str(editor.prefijo.value), len(prefijo_publicacion))
    else:
        prefijo_editor = str(editor.prefijo.value)

    return crear_ismn(prefijo_editor, prefijo_publicacion)


def almacenar_file_temporal(file):
    ruta = f"{MEDIA_ROOT}\\temp\\{file}"
    with open(ruta, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return f'/media/temp/{file}'


@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def solicitud_ismn(request):
    if request.POST:
        solicitud = Solicitud()
        solicitud.editor = Editor.objects.get(user__username=request.user)
        solicitud.temporal = request.POST.copy()
        solicitud.temporal['ismn'] = generar_ismn(solicitud.editor)
        try:
            imagen_file = request.FILES['publication_image']
            solicitud.temporal['publication_image'] = almacenar_file_temporal(imagen_file)
        except MultiValueDictKeyError:
            solicitud.temporal['publication_image'] = ''
        letra_file = request.FILES['publication_letter']
        solicitud.temporal['publication_letra'] = almacenar_file_temporal(letra_file)
        solicitud.tipo = "Solicitud-ISMN"
        solicitud.status = "Pendiente"
        solicitud.save()
        messages.success(request, 'Su solicitud se ha enviado correctamente, pronto se '
                                  'le enviará un reporte de su publicación junto al ISMN asignado.')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'solicitudes/solicitud-ISMN.html')


def send_code_confirmation(request):
    confirmation_code = randint(1000, 9999)
    print(confirmation_code)
    context = {
        'nombre': request.POST.get('first_name'),
        'code': confirmation_code
    }
    message = loader.render_to_string('emails/mail_confirmation_client.html', context)
    email = EmailMultiAlternatives(
        "Confirmación de Correo", message,
        "CCL de Cuba",
        [request.POST.get('email')],
    )
    email.content_subtype = 'html'
    try:
        email.send()
        return confirmation_code
    except TimeoutError or SMTPServerDisconnected:
        messages.error(request, 'Error en la conexión. Intente más tarde.')
        return HttpResponseRedirect('/')


def send_info_inscripcion(nombre, user_email, username, password):
    context = {
        'nombre': nombre,
        'username': username,
        'password': password
    }
    message = loader.render_to_string('emails/accept_inscription.html', context)
    email = EmailMultiAlternatives(
        "Solicitud de inscripción aceptada", message,
        "CCL de Cuba",
        [user_email],
    )
    email.content_subtype = 'html'
    try:
        email.send()
        return True
    except TimeoutError or SMTPServerDisconnected or SMTPAuthenticationError:
        return False


def send_solicitud_ismn_accepted(user, publicacion):
    context = {
        'nombre': publicacion.editor.user.first_name,
    }

    message = loader.render_to_string('emails/accept_solicitud_ismn.html', context)

    email = EmailMultiAlternatives(
        "Solicitud ISMN aceptada", message,
        "CCL de Cuba",
        [publicacion.editor.user.email],
    )
    email.content_subtype = 'html'

    # Generar el reporte y saber su ruta
    ruta = save_temporal_doc_documentation(user, publicacion)

    # Leer el archivo PDF en modo binario
    with open(ruta, "rb") as archivo_pdf:
        contenido_pdf = archivo_pdf.read()

    # Crear un objeto MIMEBase
    archivo_adjunto = MIMEBase('application', 'octet-stream')
    archivo_adjunto.set_payload(contenido_pdf)

    # Codificar el archivo adjunto en base64
    encoders.encode_base64(archivo_adjunto)

    # Establecer las cabeceras del archivo adjunto
    archivo_adjunto.add_header('Content-Disposition', f'attachment; filename="{ruta.name}"')

    email.attach(archivo_adjunto)
    try:
        email.send()
        return True
    except TimeoutError or SMTPServerDisconnected or SMTPAuthenticationError:
        return False


def crear_doc_publicacion(user, publication):
    # Importar las fuentes externas
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoSlab', 'fonts/RobotoSlab-VariableFont_wght.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', 'fonts/RobotoCondensed-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto', 'fonts/RobotoCondensed-Regular.ttf'))

    PAGE_WIDTH, PAGE_HEIGHT = A4
    style_letra = ParagraphStyle(name='letra_style', rightIndent=25, fontName="Roboto")
    style_description = ParagraphStyle(name='description_style', rightIndent=15, leading=15, fontName="Roboto")
    letra = Paragraph(f'<u><a href="http://127.0.0.1:8000/{publication.letra.url}" '
                      f'color="blue">http://127.0.0.1:8000/{publication.letra.url}</a></u>', style_letra)

    if publication.imagen.name == 'default.jpg':
        cover_title = publication.imagen.name
    else:
        cover_title = publication.imagen.name[13:]

    cover = Paragraph(f'<u><a href="http://127.0.0.1:8000/{publication.imagen.url}" '
                      f'color="blue">{cover_title}</a></u>', style_letra)

    if publication.description:
        descripcion = Paragraph(f'<font name="RobotoCondensed-Bold" '
                                f'color={colors.Color(0.21, 0.25, 0.33)}>DESCRIPCIÓN</font>'
                                f'<br/><font color={colors.Color(0.21, 0.25, 0.33)}>{publication.description}</font>',
                                style_description)
    else:
        descripcion = Paragraph(f'<font name="RobotoCondensed-Bold" '
                                f'color={colors.Color(0.21, 0.25, 0.33)}>DESCRIPCIÓN</font>'
                                f'<br/>'
                                f'<font name="Roboto-Italic" size=8 color={colors.Color(0.49, 0.30, 0.34)}>'
                                f'(Descripción opcional de la obra, breve historia de su realización y datos adicionales)</font>',
                                style_description)
    data = [['AUTOR', publication.autor],
            ['NOMBRE', publication.name],
            ['GÉNERO', publication.gender],
            ['EDITOR', publication.editor],
            ['LETRA DE LA CANCIÓN', letra, ''],
            ['ISMN', publication.ismn, descripcion],
            ['COVER', cover, ''],
            ['FECHA DE PUBLICACIÓN', publication.created_at.date(), ''],
            ['FECHA DE REALIZACIÓN',
             f'{publication.date_time.year}-{publication.date_time.month}-{publication.date_time.day}', ''],
            ['DERECHOS DE AUTOR', 'EN VENTA', '']
            ]

    def myPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, 600, 900, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, 810, 600, 50, stroke=0, fill=1)
        # Imprimir el Logo de la empresa
        canvas.drawImage('media/logo.jpg', (PAGE_WIDTH - 80) / 2, 685, 80, 110)
        # Crear encabezado del reporte
        publication_info_textobject = canvas.beginText()
        texto_encabezado = 'INFORMACIÓN DE LA PUBLICACIÓN'
        width_texto_encabezado = canvas.stringWidth(texto_encabezado, 'RobotoCondensed-Bold', 15)
        origin_start = (PAGE_WIDTH - width_texto_encabezado) / 2
        publication_info_textobject.setTextOrigin(origin_start, 665)
        publication_info_textobject.setFont('RobotoCondensed-Bold', 15)
        publication_info_textobject.setFillColorRGB(0.21, 0.25, 0.33)
        publication_info_textobject.setCharSpace(0.4)
        publication_info_textobject.textLine(texto_encabezado)
        # Titulo de la publicacion
        width_title_publicaction = canvas.stringWidth(publication.name, 'RobotoSlab', 30)
        origin_start = PAGE_WIDTH / 2 - width_title_publicaction / 2
        publication_info_textobject.setTextOrigin(origin_start, 626)
        publication_info_textobject.setFont('RobotoSlab', 30)
        publication_info_textobject.setFillColorRGB(0.49, 0.30, 0.34)
        publication_info_textobject.textLine(publication.name)
        canvas.drawText(publication_info_textobject)
        # Raya separadora
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(50, 600, 500, 4, stroke=0, fill=1)
        # Content
        publication_detail = canvas.beginText()
        publication_detail.setTextOrigin(50, 560)
        publication_detail.setFont('RobotoCondensed-Bold', 11)
        publication_detail.setCharSpace(0.25)
        publication_detail.setFillColorRGB(0.21, 0.25, 0.33)
        publication_detail.textLine('DETALLES Y AUTORÍA')
        canvas.drawText(publication_detail)
        # **--Primera Tabla - Autoria--**
        table_autoria = Table(data[:4], colWidths=[50, 400])
        table_autoria_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                          ('FONT', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
                                          ('FONT', (1, 0), (1, -1), 'Roboto'),
                                          ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
                                          ('LINEBEFORE', (1, 0), (1, -1), 0, colors.Color(1, 0, 0, alpha=0))
                                          ])
        table_autoria.setStyle(table_autoria_style)
        table_autoria.wrapOn(canvas, 50, 475)
        table_autoria.drawOn(canvas, 50, 475)
        # **--Segunda Tabla - Descripcion--**
        # Encabezado
        publication_detail.setTextOrigin(50, 448)
        publication_detail.textLine('DESCRIPCIÓN DE LA OBRA')
        canvas.drawText(publication_detail)
        # Tabla Descripción
        table_description_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                              ('VALIGN', (0, -1), (1, -1), 'TOP'),
                                              ('VALIGN', (-1, 1), (-1, 1), 'TOP'),
                                              ('TOPPADDING', (-1, 1), (-1, 1), 5),
                                              ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                                              ('FONT', (0, 0), (-1, -1), 'Roboto'),
                                              ('FONT', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
                                              ('FONT', (1, 5), (1, 5), 'RobotoCondensed-Bold'),
                                              ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
                                              ('LINEBEFORE', (1, 0), (1, -1), 0, colors.Color(1, 0, 0, alpha=0)),
                                              ('LINEBEFORE', (1, 5), (1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('BOX', (0, 1), (1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('LINEABOVE', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34)),
                                              ('SPAN', (1, 0), (2, 0)),
                                              ('SPAN', (2, 1), (2, -1))
                                              ])

        table_description = Table(data[4:], colWidths=[120, 120, 260], rowHeights=[None, None, None, None, None, 70])
        table_description.setStyle(table_description_style)
        w, h = table_description.wrapOn(canvas, 50, 275)
        x_coord_table_description = 50
        y_coord_table_description = 435 - h
        table_description.drawOn(canvas, x_coord_table_description, y_coord_table_description)
        # CheckBoxes
        x_checkbox = 57
        y_checkbox = y_coord_table_description + 30
        canvas.acroForm.checkbox(x=x_checkbox, y=y_checkbox, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox, y=y_checkbox - 16, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34, alpha=0.1), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox + 120, y=y_checkbox, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34), borderWidth=0.5)
        canvas.acroForm.checkbox(x=x_checkbox + 120, y=y_checkbox - 16, size=12,
                                 fillColor=colors.Color(0.94, 0.94, 0.94, alpha=0.1),
                                 borderColor=colors.Color(0.49, 0.30, 0.34, alpha=0.1), borderWidth=0.5)
        options = canvas.beginText()
        # Opciones 'privado y publico' de "Derechos de Autor"
        # Publico
        options.setTextOrigin(x_checkbox + 15, y_checkbox + 3)
        options.setFont('Roboto', 10)
        options.textLine('público')
        canvas.drawText(options)
        # Privado
        options.setTextOrigin(x_checkbox + 15, y_checkbox - 12)
        options.textLine('privado')
        canvas.drawText(options)
        # Opciones si y no de 'EN VENTA'
        # Si
        options.setTextOrigin(x_checkbox + 135, y_checkbox + 3)
        options.textLine('si')
        canvas.drawText(options)
        # No
        options.setTextOrigin(x_checkbox + 135, y_checkbox - 12)
        options.textLine('no')
        canvas.drawText(options)

        # Imagen del codigo de barras al final del reporte
        barcode = Image(publication.barcode.path, width=150, height=120)
        w, h = barcode.wrapOn(canvas, 350, 120)
        barcode.drawOn(canvas, 360, y_coord_table_description - h - 20)

        # Text url from cover
        cover_style = ParagraphStyle(name='style', fontName="Roboto")
        cover_url = Paragraph(f'<u><a href="http://127.0.0.1:8000/{publication.barcode.url}" '
                              f'color="blue">Mostrar Imagen</a></u>', cover_style)
        w = canvas.stringWidth('Mostrar Imagen', 'Roboto', 10)
        cover_url.wrapOn(canvas, 88, 12)
        cover_url.drawOn(canvas, 432 - w / 2, y_coord_table_description - h - 40)

        # Texto Informativo
        text_info_style = ParagraphStyle(name='text_info_style')
        text_info = Paragraph(f'<font name="Roboto-Italic" size=8 color={colors.Color(0.49, 0.30, 0.34)}>'
                              f'El reciente documento que muestra los datos principales de la publicación musical '
                              f'emerge como una herramienta esencial para el equipo y las partes interesadas. '
                              f'Al encapsular la inspiración artística, la partitura, descripción y '
                              f'datos biográficos, sirve como guía integral para comprender y comunicar '
                              f'el proyecto de publicación. Este recurso clave garantiza un impacto positivo en todos '
                              f'los aspectos de la iniciativa musical, y se espera compartir más detalles en el futuro.</font>',
                              text_info_style)
        w, h = text_info.wrapOn(canvas, 200, 200)
        y_coord_text_info = y_coord_table_description - h - 20
        text_info.drawOn(canvas, 50, y_coord_text_info)

        # Tabla de Reportado por:
        # Datos
        if user.especialista:
            departamento = 'Informatica - CCL'
        else:
            departamento = '-'
        data_table_report_by = [
            ['REPORTADO POR:', ''],
            ['Nombre:', user.first_name],
            ['Fecha:', datetime.today().date()],
            ['Departamento:', departamento]
        ]
        report_by_style = TableStyle(
            [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('ALIGN', (1, 0), (1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
             ('FONTNAME', (1, 0), (1, -1), 'Roboto'),
             ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
             ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34))]
        )
        table_report_by = Table(data_table_report_by, colWidths=[100, 140], style=report_by_style)
        w, h = table_report_by.wrapOn(canvas, 400, 200)
        table_report_by.drawOn(canvas, 50, y_coord_text_info - h - 15)

        # Footer
        # Raya separadora
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(50, 50, 500, 4, stroke=0, fill=1)
        # Barra final
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, 0, 600, 10, stroke=0, fill=1)
        canvas.restoreState()

    return myPage


def export_musical_publication(request, musical_publication_id):
    # Tomar la Info. de la Publicación a exportar
    publication = Musical_Publication.objects.get(id=musical_publication_id)

    # Crear el temporal para el pdf
    buffer = io.BytesIO()
    # Contenido del reporte
    mypage = crear_doc_publicacion(request.user, publication)

    story = [Spacer(1, 2 * inch)]
    doc = SimpleDocTemplate(buffer)
    doc.build(story, onFirstPage=mypage)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{publication.name}.pdf")


def extraer_datos_model(modelo_list):
    # Saber con que tipo de modelo estamos trabajando:
    modelo_type = modelo_list.model._meta.model_name
    contenido = dict()

    if modelo_type == 'musical_publication':
        contenido['ID'] = [publicacion.id for publicacion in modelo_list]
        contenido['Título'] = [publicacion.name for publicacion in modelo_list]
        contenido['Autor'] = [publicacion.autor for publicacion in modelo_list]
        contenido['Editor'] = [publicacion.editor.user.first_name for publicacion in modelo_list]
        contenido['ISMN'] = [publicacion.ismn for publicacion in modelo_list]
        contenido['Fecha'] = [publicacion.date_time.strftime('%Y-%m-%d') for publicacion in modelo_list]
        contenido['Género'] = [publicacion.gender for publicacion in modelo_list]
    elif modelo_type == 'editor':
        contenido['ID'] = [editor.id for editor in modelo_list]
        contenido['Tipo'] = [editor.type for editor in modelo_list]
        contenido['Nombre'] = [editor.user.first_name for editor in modelo_list]
        contenido['ID Tributaria'] = [editor.id_tribute for editor in modelo_list]
        contenido['Prefijo'] = [editor.prefijo for editor in modelo_list]
        contenido['Estado'] = [editor.get_state_display() for editor in modelo_list]
        contenido['Dirección'] = [editor.directions for editor in modelo_list]
        contenido['Teléfono'] = [editor.phone for editor in modelo_list]
    elif modelo_type == 'solicitud':
        contenido['ID'] = [solicitud.id for solicitud in modelo_list]
        contenido['Editor'] = [solicitud.editor.user.first_name if solicitud.editor else '-' for solicitud in
                               modelo_list]
        contenido['Solicitante'] = [solicitud.temporal['first_name'] if solicitud.tipo == 'Solicitud-Inscripción'
                                                                        and solicitud.status == 'Pendiente' else '-'
                                    for solicitud in modelo_list]
        contenido['Fecha'] = [solicitud.created_at.strftime('%Y-%m-%d') for solicitud in modelo_list]
        contenido['Tipo'] = [solicitud.tipo for solicitud in modelo_list]
        contenido['Estado'] = [solicitud.status for solicitud in modelo_list]
    else:
        pass
    return contenido


def crear_report_list(model_list, buffer):
    #  --- Datos del modelo que queremos reportar ---
    # Datos de la Tabla
    diccionario = extraer_datos_model(model_list)
    # Tipo de Modelo (Editor, Publicacion, Solicitud)
    tipo = model_list.model.__name__
    # Titulo de la primera pagina, tipo de modelo a reportar
    title = str()
    # Ancho de las columnas de la tabla
    col_widths = list()
    if tipo == "Musical_Publication":
        title = 'Publicaciones Musicales'
        col_widths = [30, 120, 120, 110, 110, 110]
    elif tipo == 'Editor':
        title = 'Editores'
        col_widths = [30, 90, 120, 90, 60, 50, 160, 90]
    else:
        title = 'Solicitudes'
        col_widths = [30, 130, 130, 100, 115, 110]

    # Importar las fuentes externas
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoSlab', 'fonts/RobotoSlab-VariableFont_wght.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', 'fonts/RobotoCondensed-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto', 'fonts/RobotoCondensed-Regular.ttf'))

    PAGE_HEIGHT, PAGE_WIDTH = A4
    style_letra = ParagraphStyle(name='letra_style', rightIndent=25, fontName="Roboto")

    def myFirstPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, PAGE_HEIGHT - 31, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        # Imprimir el Logo de la empresa
        img_h = 110
        img_w = 80
        canvas.drawImage('media/logo.jpg', (PAGE_WIDTH - img_w) / 2, PAGE_HEIGHT - 155, img_w, img_h)
        # Crear encabezado del reporte
        publication_info_textobject = canvas.beginText()
        texto_encabezado = 'LISTADO DE BASE DE DATOS'
        width_texto_encabezado = canvas.stringWidth(texto_encabezado, 'RobotoCondensed-Bold', 15)
        origin_start = (PAGE_WIDTH - width_texto_encabezado) / 2
        publication_info_textobject.setTextOrigin(origin_start, PAGE_HEIGHT - 175)
        publication_info_textobject.setFont('RobotoCondensed-Bold', 15)
        publication_info_textobject.setFillColorRGB(0.21, 0.25, 0.33)
        publication_info_textobject.setCharSpace(0.4)
        publication_info_textobject.textLine(texto_encabezado)
        # Titulo del listado
        width_title_publicaction = canvas.stringWidth(title, 'RobotoSlab', 30)
        origin_start = (PAGE_WIDTH - width_title_publicaction) / 2
        publication_info_textobject.setTextOrigin(origin_start, PAGE_HEIGHT - 215)
        publication_info_textobject.setFont('RobotoSlab', 30)
        publication_info_textobject.setFillColorRGB(0.49, 0.30, 0.34)
        publication_info_textobject.textLine(title)
        canvas.drawText(publication_info_textobject)
        # Raya separadora inicial
        w_rect = 740
        h_rect = 4
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 241, w_rect, h_rect, stroke=0, fill=1)
        # Raya separadora final
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 550, w_rect, h_rect, stroke=0, fill=1)
        canvas.restoreState()

    def myLaterPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, PAGE_HEIGHT - 31, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

        # Imprimir el Logo de la empresa transparente
        img_h = 440
        img_w = 320
        canvas.drawImage('media/logo_transparent.png', (PAGE_WIDTH - img_w) / 2, (PAGE_HEIGHT - img_h) / 2, img_w,
                         img_h, mask='auto')
        # Raya separadora inicial
        w_rect = 740
        h_rect = 4
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 65, w_rect, h_rect, stroke=0, fill=1)
        # Numeracion de Paginas
        page_number = canvas.beginText()
        page_number.setTextOrigin(inch, 0.90 * inch)
        page_number.setFont('RobotoSlab', 10)
        page_number.setFillColorRGB(0.49, 0.30, 0.34)
        page_number.textLine("Página %s" % doc.page)
        canvas.drawText(page_number)
        # Raya separadora final
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 550, w_rect, h_rect, stroke=0, fill=1)
        canvas.restoreState()

    def build_doc(pbuffer):
        # Datos para conformar el documento
        doc = SimpleDocTemplate(pbuffer, pagesize=landscape(A4))

        story = [Spacer(PAGE_WIDTH - 545, PAGE_HEIGHT - 400)]
        style_table = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONT', (0, 0), (-1, 0), 'RobotoCondensed-Bold'),
                                  ('FONT', (0, 1), (-1, -1), 'Roboto'),
                                  ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
                                  ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34))
                                  ])

        # Conformar los datos para la tabla de ReportLab
        # Obtener todas las llaves
        llaves = list(diccionario.keys())
        # Crear la lista resultante
        datas = [llaves]
        # Obtener el número de elementos del modelo
        num_elementos = len(list(diccionario.values())[0])
        # Iterar sobre los elementos
        for i in range(num_elementos):
            fila = []
            for llave in llaves:
                valor = diccionario[llave][i]
                fila.append(valor)
            datas.append(fila)
        # TABLE
        table = Table(datas, colWidths=col_widths)
        table.setStyle(style_table)
        story.append(table)
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPage)

    build_doc(buffer)


def export_publications_list(request):
    # Crear el temporal para el pdf
    buffer = io.BytesIO()

    # Filtros de exportacion
    titulo_filter = request.POST['titulo'] if request.POST['titulo'] else None
    autor_filter = request.POST['autor'] if request.POST['autor'] else None
    editor_filter = request.POST['editor'] if request.POST['editor'] else None
    genero_filter = request.POST['genero'] if request.POST['genero'] != 'Todos' else None
    fecha_publicacion_filter = request.POST['fecha'] if request.POST['fecha'] else None
    orden_filter = bool('orden' in request.POST)
    cantidades = {
        '0': 1,
        '1': 10,
        '2': 25,
        '3': 40,
        '4': None
    }
    cantidad_filter = cantidades.get(request.POST.get('cant_element'), None)
    filters = {
        'name__icontains': titulo_filter,
        'autor__icontains': autor_filter,
        'editor__user__first_name__icontains': editor_filter,
        'gender__icontains': genero_filter,
        'date_time__gte': fecha_publicacion_filter
    }

    # Lista completa de editores en orden LIFO
    list_publications = Musical_Publication.objects.all().order_by('-id')

    # Aplicando los filtros a la lista de Publicaciones
    for key, value in filters.items():
        if value:
            list_publications = list_publications.filter(**{key: value})

    if not orden_filter:
        list_publications = list_publications.order_by('id')
    if cantidad_filter and len(list_publications) >= cantidad_filter:
        list_publications = list_publications.all()[:cantidad_filter]

    crear_report_list(list_publications, buffer)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Publicaciones_lista.pdf")


def export_editores_list(request):
    # Crear el temporal para el pdf
    buffer = io.BytesIO()

    # Filtros de exportacion
    tipo_editor_filter = request.POST['flexRadioTipo'] if request.POST['flexRadioTipo'] != 'Ambos' else None
    fecha_inscripcion_filter = request.POST['fecha'] if request.POST['fecha'] else None
    nombre_filter = request.POST['nombre'] if request.POST['nombre'] else None
    rango_filter = request.POST['rango'] if request.POST['rango'] != 'Todos' else None
    activo_filter = bool('activo' in request.POST)
    orden_filter = bool('orden' in request.POST)
    cantidades = {
        '0': 1,
        '1': 10,
        '2': 25,
        '3': 40,
        '4': None
    }
    cantidad_filter = cantidades.get(request.POST.get('cant_element'), None)
    filters = {
        'type': tipo_editor_filter,
        'user__date_joined__gte': fecha_inscripcion_filter,
        'user__first_name__icontains': nombre_filter,
        'prefijo__rango__rango_superior': rango_filter,

    }

    # Lista completa de editores en orden LIFO
    list_editores = Editor.objects.all().order_by('-id')

    # Aplicando los filtros a la lista de Editores
    for key, value in filters.items():
        if value:
            list_editores = list_editores.filter(**{key: value})
    if not activo_filter:
        list_editores = list_editores.filter(state=False)
    if not orden_filter:
        list_editores = list_editores.order_by('id')
    if cantidad_filter and len(list_editores) >= cantidad_filter:
        list_editores = list_editores.all()[:cantidad_filter]

    crear_report_list(list_editores, buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Editores_lista.pdf")


def export_solicitudes_list(request):
    # Crear el temporal para el pdf
    buffer = io.BytesIO()

    # Filtros de exportacion
    editor_filter = request.POST['sol_editor'] if request.POST['sol_editor'] else None
    fecha_filter = request.POST['fecha'] if request.POST['fecha'] else None
    tipo_filter = request.POST['tipo'] if request.POST['tipo'] != 'Todos' else None
    estado_filter = request.POST['estado'] if request.POST['estado'] != 'Ambos' else None
    orden_filter = bool('orden' in request.POST)
    cantidades = {
        '0': 1,
        '1': 10,
        '2': 25,
        '3': 40,
        '4': None
    }
    cantidad_filter = cantidades.get(request.POST['cant_element'], None)
    filters = {
        'editor__user__first_name__icontains': editor_filter,
        'created_at__gte': fecha_filter,
        'tipo': tipo_filter,
        'status': estado_filter
    }

    # Lista completa de solicitudes en orden LIFO
    list_solicitudes = Solicitud.objects.all().order_by('-id')

    # Aplicando los filtros a la lista de Solicitudes
    for key, value in filters.items():
        if value:
            list_solicitudes = list_solicitudes.filter(**{key:value})
    if not orden_filter:
        list_solicitudes = list_solicitudes.order_by('id')
    if cantidad_filter and len(list_solicitudes) >= cantidad_filter:
        list_solicitudes = list_solicitudes.all()[:cantidad_filter]

    crear_report_list(list_solicitudes, buffer)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Solicitudes_lista.pdf")


def save_temporal_doc_documentation(user, publication):
    ruta = Path(f"{MEDIA_ROOT}/temp/{publication.name}.pdf")
    doc = SimpleDocTemplate(ruta.__str__())
    story = [Spacer(1, 2 * inch)]
    mypage = crear_doc_publicacion(user, publication)
    doc.build(story, onFirstPage=mypage)
    return ruta


def agregar_fondo_save(imagen_binaria, output_path):
    # Abrir la imagen
    imagen = PILImage.open(io.BytesIO(imagen_binaria))

    # Crear una nueva imagen con fondo blanco del mismo tamaño que la original
    imagen_con_fondo_blanco = PILImage.new("RGBA", imagen.size, (240, 240, 240))

    # Pegar la imagen original en la imagen con fondo blanco
    imagen_con_fondo_blanco.paste(imagen, (0, 0), imagen)

    # Guardar la imagen con fondo blanco
    imagen_con_fondo_blanco.save(output_path)


def conformar_tabla_reportlab_solicitudes_aceptadas(solicites):
    data = [['FECHA', 'TIPO', 'CANTIDAD']]
    total = 0

    for fecha, tipos in solicites.items():
        fecha_str = fecha.strftime('%d/%m')
        for tipo, cantidad in tipos.items():
            if tipo == 'Solicitud-ISMN':
                data.append([fecha_str, tipo, cantidad])
            else:
                data.append(['-', tipo, cantidad])
            total += cantidad
    data.append(['', 'TOTAL', total])
    return data


def crear_report_statistics(buffer, title, total_solicitudes_enviadas, user):
    # Importar las fuentes externas
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoSlab', 'fonts/RobotoSlab-VariableFont_wght.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', 'fonts/RobotoCondensed-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto', 'fonts/RobotoCondensed-Regular.ttf'))

    PAGE_HEIGHT, PAGE_WIDTH = A4
    style_letra = ParagraphStyle(name='letra_style', rightIndent=25, fontName="Roboto")

    # Datos para la tabla de reportlab
    solicitudes_enviadas = dict(list(Solicitud.return_accepted().items())[-7:])

    data = conformar_tabla_reportlab_solicitudes_aceptadas(solicitudes_enviadas)

    def myFirstPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, PAGE_HEIGHT - 31, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        # Imprimir el Logo de la empresa
        img_h = 110
        img_w = 80
        canvas.drawImage('media/logo.jpg', (PAGE_WIDTH - img_w) / 2, PAGE_HEIGHT - 155, img_w, img_h)
        # Crear encabezado del reporte
        publication_info_textobject = canvas.beginText()
        texto_encabezado = 'REPORTES Y ESTADÍSTICAS'
        width_texto_encabezado = canvas.stringWidth(texto_encabezado, 'RobotoCondensed-Bold', 15)
        origin_start = (PAGE_WIDTH - width_texto_encabezado) / 2
        publication_info_textobject.setTextOrigin(origin_start, PAGE_HEIGHT - 175)
        publication_info_textobject.setFont('RobotoCondensed-Bold', 15)
        publication_info_textobject.setFillColorRGB(0.21, 0.25, 0.33)
        publication_info_textobject.setCharSpace(0.4)
        publication_info_textobject.textLine(texto_encabezado)
        # Titulo del listado
        width_title_publicaction = canvas.stringWidth(title, 'RobotoSlab', 30)
        origin_start = (PAGE_WIDTH - width_title_publicaction) / 2
        publication_info_textobject.setTextOrigin(origin_start, PAGE_HEIGHT - 215)
        publication_info_textobject.setFont('RobotoSlab', 30)
        publication_info_textobject.setFillColorRGB(0.49, 0.30, 0.34)
        publication_info_textobject.textLine(title)
        canvas.drawText(publication_info_textobject)
        # Raya separadora inicial
        w_rect = 740
        h_rect = 4
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 241, w_rect, h_rect, stroke=0, fill=1)
        # Chart 1
        img_h = 300
        img_w = 350
        canvas.drawImage('media/temp/linechart_solicitudes.png', PAGE_WIDTH - 790, PAGE_HEIGHT - img_h - 255, img_w, img_h)
        # Text from Chart 1
        # Icon
        d = Drawing(100, 100)
        icon = signsandsymbols.NotAllowed()
        icon.fillColor = colors.Color(0.94, 0.94, 0.94)
        icon.strokeColor = colors.Color(0.21, 0.25, 0.33)
        icon.size = 40
        d.add(icon)
        d.drawOn(canvas, PAGE_WIDTH - 400, PAGE_HEIGHT - 345)
        # Title
        solicitudes_declined = canvas.beginText()
        solicitudes_declined_title = 'Solicitudes rechazadas.'
        origin_start = PAGE_WIDTH - 355
        solicitudes_declined.setTextOrigin(origin_start, PAGE_HEIGHT - 330)
        solicitudes_declined.setFont('RobotoSlab', 20)
        solicitudes_declined.setFillColorRGB(0.21, 0.25, 0.33)
        solicitudes_declined.setCharSpace(0.4)
        solicitudes_declined.textLine(solicitudes_declined_title)
        canvas.drawText(solicitudes_declined)
        # Paragraph
        style_description_chart1 = ParagraphStyle(name='description_style_chart1', leading=17)
        text_info = Paragraph(f'<font name="Roboto-Italic" size=12 color={colors.Color(0.49, 0.30, 0.34)}>'
                              f'Esta gráfica muestra la cantidad de solicitudes<br/>'
                              f'rechazadas en los últimos meses según su tipo<br/>'
                              f'(ISMN ó Inscripción).</font>',
                              style_description_chart1)
        w, h = text_info.wrapOn(canvas, 300, 200)
        text_info.drawOn(canvas, origin_start, PAGE_HEIGHT - h - 337)
        # Total
        solicitudes_declined_total = canvas.beginText()
        solicitudes_declined_total_title = f'Total: {Solicitud.return_deleted().count()}'
        solicitudes_declined_total.setTextOrigin(origin_start, PAGE_HEIGHT - h - 380)
        solicitudes_declined_total.setFont('RobotoSlab', 20)
        solicitudes_declined_total.setFillColorRGB(0.21, 0.25, 0.33)
        solicitudes_declined_total.setCharSpace(0.4)
        solicitudes_declined_total.textLine(solicitudes_declined_total_title)
        canvas.drawText(solicitudes_declined_total)

        # Raya separadora final
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 570, w_rect, h_rect, stroke=0, fill=1)
        canvas.restoreState()

    def myLaterPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.rect(0, PAGE_HEIGHT - 31, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        # Raya separadora inicial
        w_rect = 740
        h_rect = 4
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 65, w_rect, h_rect, stroke=0, fill=1)
        # Imprimir el CHART 2
        im_width = 350
        im_height = 300
        im = Image('media/temp/barchart_solicitudes.png', width=im_width, height=im_height)
        im.drawOn(canvas, PAGE_WIDTH - 790, (PAGE_HEIGHT - im_height)/2 + 50)
        # Title Chart 2
        solicitudes_enviadas = canvas.beginText()
        solicitudes_enviadas_title = 'Solicitudes Enviadas.'
        solicitudes_enviadas.setTextOrigin(inch, PAGE_HEIGHT - im_height - 120)
        solicitudes_enviadas.setFont('RobotoSlab', 20)
        solicitudes_enviadas.setFillColorRGB(0.21, 0.25, 0.33)
        solicitudes_enviadas.setCharSpace(0.4)
        solicitudes_enviadas.textLine(solicitudes_enviadas_title)
        canvas.drawText(solicitudes_enviadas)
        # Paragraph
        style_description_chart1 = ParagraphStyle(name='description_style_chart1', leading=17)
        text_info = Paragraph(f'<font name="Roboto-Italic" size=12 color={colors.Color(0.49, 0.30, 0.34)}>'
                              f'Esta gráfica muestra la cantidad de solicitudes<br/>'
                              f'enviadas en el último mes.</font>',
                              style_description_chart1)
        w, h = text_info.wrapOn(canvas, 300, 200)
        text_info.drawOn(canvas, inch, PAGE_HEIGHT - im_height - h - 130)
        # Total
        solicitudes_declined_total = canvas.beginText()
        solicitudes_declined_total_title = f'Total: {total_solicitudes_enviadas}'
        solicitudes_declined_total.setTextOrigin(inch, PAGE_HEIGHT - im_height - h - 170)
        solicitudes_declined_total.setFont('RobotoSlab', 20)
        solicitudes_declined_total.setFillColorRGB(0.21, 0.25, 0.33)
        solicitudes_declined_total.setCharSpace(0.4)
        solicitudes_declined_total.textLine(solicitudes_declined_total_title)
        canvas.drawText(solicitudes_declined_total)
        # Table Solicitudes Aceptadas
        table_style = TableStyle(
            [('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
             ('FONTNAME', (1, 0), (-1, 0), 'RobotoCondensed-Bold'),
             ('FONTNAME', (1, 1), (-1, -1), 'Roboto'),
             ('FONTNAME', (1, -1), (-1, -1), 'RobotoCondensed-Bold'),
             ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
             ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0, 0, 0, alpha=0.1)),
             ]
        )
        table = Table(data, colWidths=[80, 140, 80], style=table_style)
        w, h = table.wrapOn(canvas, 300, 800)
        table.drawOn(canvas, PAGE_WIDTH + im_width - 770, (PAGE_HEIGHT-h)/2 + 52)
        # Title Table Solicitudes Aceptadas
        solicitudes_aceptadas = canvas.beginText()
        solicitudes_aceptadas_title = 'Solicitudes Aceptadas.'
        solicitudes_aceptadas.setTextOrigin(PAGE_WIDTH + im_width - 770, PAGE_HEIGHT - im_height - 120)
        solicitudes_aceptadas.setFont('RobotoSlab', 20)
        solicitudes_aceptadas.setFillColorRGB(0.21, 0.25, 0.33)
        solicitudes_aceptadas.setCharSpace(0.4)
        solicitudes_aceptadas.textLine(solicitudes_aceptadas_title)
        canvas.drawText(solicitudes_aceptadas)
        # Paragraph
        style_description_chart1 = ParagraphStyle(name='description_style_chart1', leading=17)
        text_info = Paragraph(f'<font name="Roboto-Italic" size=12 color={colors.Color(0.49, 0.30, 0.34)}>'
                              f'Esta tabla muestra la cantidad de solicitudes<br/>'
                              f'aceptadas en la última semana.</font>',
                              style_description_chart1)
        w, h = text_info.wrapOn(canvas, 300, 200)
        text_info.drawOn(canvas, PAGE_WIDTH + im_width - 770, PAGE_HEIGHT - im_height - h - 130)
        # Tabla de Reportado por:
        # Datos
        if user.especialista:
            departamento = 'Informatica - CCL'
        else:
            departamento = '-'
        data_table_report_by = [
            ['REPORTADO POR:', ''],
            ['Nombre:', user.first_name],
            ['Fecha:', datetime.today().date()],
            ['Departamento:', departamento]
        ]
        report_by_style = TableStyle(
            [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('ALIGN', (1, 0), (1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (0, -1), 'RobotoCondensed-Bold'),
             ('FONTNAME', (1, 0), (1, -1), 'Roboto'),
             ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.21, 0.25, 0.33)),
             ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.49, 0.30, 0.34))]
        )
        table_report_by = Table(data_table_report_by, colWidths=[100, 140], style=report_by_style)
        w, h = table_report_by.wrapOn(canvas, 400, 200)
        table_report_by.drawOn(canvas, PAGE_WIDTH - w - 60, PAGE_HEIGHT - im_height - h - 195)

        # Numeracion de Paginas
        page_number = canvas.beginText()
        page_number.setTextOrigin(inch, PAGE_HEIGHT - 560)
        page_number.setFont('RobotoSlab', 10)
        page_number.setFillColorRGB(0.49, 0.30, 0.34)
        page_number.textLine("Página %s" % doc.page)
        canvas.drawText(page_number)
        # Raya separadora final
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(PAGE_WIDTH - 790, PAGE_HEIGHT - 580, w_rect, h_rect, stroke=0, fill=1)
        canvas.restoreState()

    def build_doc(pbuffer):
        # Datos para conformar el documento
        doc = SimpleDocTemplate(pbuffer, pagesize=landscape(A4))
        story = [Spacer(PAGE_WIDTH - 545, PAGE_HEIGHT - 400)]
        # ====--- Content ----====
        story.append(PageBreak())
        story.append(Spacer(PAGE_WIDTH - 545, PAGE_HEIGHT - 400))
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPage)

    build_doc(buffer)


def save_image_from_base64(request):
    data = json.loads(request.body)
    linechart_image_base64 = data.get('image_data_lineChart')
    barchart_image_base64 = data.get('image_data_barChart')
    image_data_linechart = linechart_image_base64.split(',')[1]
    image_data_barchart = barchart_image_base64.split(',')[1]
    image_binary_linechart = base64.b64decode(image_data_linechart)
    image_binary_barchart = base64.b64decode(image_data_barchart)
    ruta = Path(MEDIA_ROOT) / 'temp'
    agregar_fondo_save(image_binary_linechart, ruta / 'linechart_solicitudes.png')
    agregar_fondo_save(image_binary_barchart, ruta / 'barchart_solicitudes.png')


def export_statistics_solicitud(request):
    if request.method == 'POST':
        # Almacenando los graficos en imagenes
        save_image_from_base64(request)

        # Datos para la tabla
        solicitudes_aceptadas = dict(list(Solicitud.return_accepted().items())[-31:])

        buffer = io.BytesIO()
        # Contenido del reporte
        data = json.loads(request.body)
        total_solicitudes_enviadas = data.get('total_image_data_barChart')
        crear_report_statistics(buffer, 'Solicitudes', total_solicitudes_enviadas, request.user)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Solicitud_estadisticas.pdf")



