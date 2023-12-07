from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from App.models import Editor, Musical_Publication, Registered_Data
from django.views.decorators.cache import cache_control
from django.contrib import messages  # Return messages
from django.http import HttpResponseRedirect  # Redirect the page after submit
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives  # Required to send emails
from django.template import loader  # Render templates on email body
from django.contrib.auth.views import LoginView, LogoutView
import io
from django.http import FileResponse
# REPORTLAB
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


# ================= FRONTEND SECTION =================
class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    next_page = '/'


class MyLogoutView(LogoutView):
    next_page = '/'


# Registration Function
def register_user(request):
    if request.method == 'POST':
        return render(request, 'frontend.html')
    else:
        return render(request, 'registration/register_user.html')


# Function to render the Home Page
def frontend(request):
    return render(request, 'frontend.html')


# ================= BACKEND SECTION =================
# Function to render the Backend Page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_editores(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_editor_list = Editor.objects.filter(
            Q(user__username__icontains=q) | Q(user__email__icontains=q) | Q(directions__icontains=q) |
            Q(note__icontains=q) | Q(user__first_name__icontains=q)
        ).order_by('-user__date_joined')
        if q.isnumeric():
            all_editor_list = Editor.objects.filter(Q(age=q) | Q(phone__contains=q) |
                                                    Q(id_tribute=q)).order_by('-user__date_joined')
    else:
        all_editor_list = Editor.objects.all().order_by('-user__date_joined')

    paginator = Paginator(all_editor_list, 4)
    page = request.GET.get('page')
    all_editor = paginator.get_page(page)

    return render(request, 'backend.html', {"editores": all_editor})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def backend_publicaciones(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_publication_list = Musical_Publication.objects.filter(
            Q(name__icontains=q) | Q(autor__icontains=q) | Q(editor__user__username__icontains=q) |
            Q(gender__icontains=q) | Q(ismn__icontains=q)
        ).order_by('-created_at')
    else:
        all_publication_list = Musical_Publication.objects.all().order_by('-created_at')

    paginator = Paginator(all_publication_list, 4)
    page = request.GET.get('page')
    all_publication = paginator.get_page(page)

    return render(request, 'publications-list.html', {"publicaciones": all_publication})


# Function to Add patient
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_editor(request):
    if request.method == 'POST':

        # Check if email exist in BD
        email = request.POST['email']
        phone = request.POST['phone']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Este teléfono ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/')
        # ===========================
        else:
            if request.POST.get('name') \
                    and request.POST.get('password') \
                    and request.POST.get('phone') \
                    and request.POST.get('email') \
                    and request.POST.get('age') \
                    and request.POST.get('gender') \
                    or request.POST.get('note'):
                editor = Editor()
                editor.name = request.POST.get('name')
                editor.password = request.POST.get('password')
                editor.phone = request.POST.get('phone')
                editor.email = request.POST.get('email')
                editor.age = request.POST.get('age')
                editor.gender = request.POST.get('gender')
                editor.note = request.POST.get('note')
                editor.save()

                # Register email and phone inside BD
                contact = Registered_Data()
                contact.email = email
                contact.phone = phone
                contact.save()
                # ========================

                messages.success(request, "Editor added successfully !")
                return HttpResponseRedirect('/backend')
    else:
        return render(request, "add.html")


# Function to delete patient
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    editor.delete()
    messages.success(request, "Editor removed succesfully !")
    return HttpResponseRedirect('/backend')


# Function to access the patient individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def editor(request, editor_id):
    editor = Editor.objects.get(id=editor_id)
    if editor:
        return render(request, "edit.html", {"editor": editor})


# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_editor(request):
    if request.method == "POST":
        editor = Editor.objects.get(id=request.POST.get('id'))
        if editor:
            editor.name = request.POST.get("name")
            editor.phone = request.POST.get("phone")
            editor.email = request.POST.get("email")
            editor.age = request.POST.get("age")
            editor.gender = request.POST.get("gender")
            editor.note = request.POST.get("note")
            editor.save()
            messages.success(request, "Editor upload successfully !")
            return HttpResponseRedirect('/backend')


# Function to show musical collections
def musical_colections_list(request):
    Musical_Collections_Objects = Musical_Publication.objects.all()
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


# Function to add a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def add_musical_publication(request):
    if request.method == 'POST':
        if request.POST.get('name') \
                and request.POST.get('autor') \
                and request.POST.get('ismn') \
                and request.POST.get('letter_contain') \
                and request.POST.get('description') \
                and request.POST.get('date_time') \
                and request.POST.get('gender') \
                or request.POST.get('imagen'):
            musical_publication = Musical_Publication()
            musical_publication.name = request.POST.get('name')
            musical_publication.autor = request.POST.get('autor')
            musical_publication.ismn = request.POST.get('ismn')
            musical_publication.letter_contain = request.POST.get('letter_contain')
            musical_publication.description = request.POST.get('description')
            musical_publication.date_time = request.POST.get('date_time')
            musical_publication.gender = request.POST.get('gender')
            musical_publication.imagen = request.FILES.get('imagen')
            musical_publication.save()
            messages.success(request, "Publicación musical añadida correctamente !")
            return HttpResponseRedirect('/backend')
    else:
        return render(request, "add_publication.html")


# Function to access the musical_publication individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    if musical_publication:
        return render(request, "edit_publication.html", {"musical_publication": musical_publication})


# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_musical_publication(request):
    if request.method == "POST":
        musical_publication = Musical_Publication.objects.get(id=request.POST.get('id'))
        if musical_publication:
            musical_publication.name = request.POST.get('name')
            musical_publication.autor = request.POST.get('autor')
            musical_publication.ismn = request.POST.get('ismn')
            musical_publication.letter_contain = request.POST.get('letter_contain')
            musical_publication.description = request.POST.get('description')
            musical_publication.date_time = request.POST.get('date_time')
            musical_publication.gender = request.POST.get('gender')
            musical_publication.imagen = request.FILES.get('imagen')
            musical_publication.save()
            messages.success(request, "Publicacion Musical actualizada correctamente !")
            return HttpResponseRedirect('/musical_colections')


# Function to delete a musical publication
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_musical_publication(request, musical_publication_id):
    musical_publication = Musical_Publication.objects.get(id=musical_publication_id)
    musical_publication.delete()
    messages.success(request, "Publicacion Musical eliminada correctamente !")
    return HttpResponseRedirect('/musical_colections')


# Function to send ISMN solicitud
def send_email_solicitud_ismn(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        descripcion = request.POST.get('descripcion')

        context = {
            'name': name,
            'age': age,
            'email': email,
            'phone': phone,
            'address': address,
            'descripcion': descripcion
        }
        message = loader.render_to_string('resume_form.html', context)
        email = EmailMultiAlternatives(
            "ISMN - Solicitud", message,
            "Editores de Cuba",
            ['antoniocruzglez24@gmail.com'],
        )

        email.content_subtype = 'html'
        file = request.FILES['file']
        email.attach(file.name, file.read(), file.content_type)
        try:
            email.send()
        except TimeoutError:
            messages.error(request, 'Error en la conexión. Intente más tarde.')
        messages.success(request, 'Solicitud ISMN enviada correctamente !')
        return HttpResponseRedirect('/')


def export_musical_publication(request, musical_publication_id):
    # Tomar la Info. de la Publicación a exportar
    publication = Musical_Publication.objects.get(id=musical_publication_id)
    # Crear el Canva
    buffer = io.BytesIO()
    # Importar las fuentes externas
    pdfmetrics.registerFont(TTFont('RobotoCondensed-Bold', 'fonts/RobotoCondensed-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('RobotoSlab', 'fonts/RobotoSlab-VariableFont_wght.ttf'))

    PAGE_WIDTH, PAGE_HEIGHT = A4
    pageinfo = f"{publication.name}"

    def myFirstPage(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, 600, 900, fill=1)
        # Barra de encabezado
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        # Imprimir el Logo de la empresa
        canvas.drawImage('media/logo.jpg', 250, 685, 80, 110)
        canvas.rect(0, 810, 700, 50, stroke=0, fill=1)
        # Crear encabezado del reporte
        publication_info_textobject = canvas.beginText()
        publication_info_textobject.setTextOrigin(175, 652)
        publication_info_textobject.setFont('RobotoCondensed-Bold', 15)
        publication_info_textobject.setFillColorRGB(0.21, 0.25, 0.33)
        publication_info_textobject.setCharSpace(0.4)
        publication_info_textobject.textLine('INFORMACIÓN DE LA PUBLICACIÓN')
        # Centrando el titulo de la publicacion
        width_title_publicaction = canvas.stringWidth(publication.name, 'RobotoSlab', 30)
        origin_start = PAGE_WIDTH/2 - width_title_publicaction/2
        publication_info_textobject.setTextOrigin(origin_start, 615)
        publication_info_textobject.setFont('RobotoSlab', 30)
        publication_info_textobject.setFillColorRGB(0.49, 0.30, 0.34)
        publication_info_textobject.textLine(publication.name)
        canvas.drawText(publication_info_textobject)
        # Raya separadora
        canvas.setFillColorRGB(0.49, 0.30, 0.34)
        canvas.rect(50, 590, 500, 4, stroke=0, fill=1)
        # Content
        publication_detail = canvas.beginText()
        publication_detail.setTextOrigin(50, 560)
        publication_detail.setFont('RobotoCondensed-Bold', 11)
        publication_detail.setCharSpace(0.25)
        publication_detail.setFillColorRGB(0.21, 0.25, 0.33)
        publication_detail.textLine('DETALLE DE LA PUBLICACIÓN')
        canvas.drawText(publication_detail)
        # Footer
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "Primera Página / %s" % datetime.today())
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        canvas.saveState()
        # Color de Fondo
        canvas.setFillColorRGB(0.94, 0.94, 0.94)
        canvas.rect(0, 0, 600, 900, fill=1)
        # Footer
        canvas.setFont('Times-Roman', 9)
        canvas.setFillColorRGB(0.21, 0.25, 0.33)
        canvas.drawString(inch, 0.75 * inch, 'Página %d / %s' % (doc.page, datetime.today()))
        canvas.restoreState()

    styles = getSampleStyleSheet()
    Story = [Spacer(1, 3*inch)]
    style = styles["Normal"]

    for i in range(10):
        bogustext = (f'<b>{request.user.username}</b> This is Paragraph number %s. ' % i) * 20
        paragraph = Paragraph(bogustext, style)
        Story.append(paragraph)
        Story.append(Spacer(1, 0.2*inch))

    doc = SimpleDocTemplate(buffer)
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


    # p.showPage()
    # p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{publication.name}.pdf")
