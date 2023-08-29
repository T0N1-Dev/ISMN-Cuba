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
from django.contrib.auth import authenticate, login


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
@login_required(login_url = "login")
def backend(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_editor_list = Editor.objects.filter(
            Q(name__icontains=q) | Q(email__icontains=q) | Q(gender__icontains=q) | Q(note__icontains=q)
        ).order_by('-created_at')
        if q.isnumeric():
            all_editor_list = Editor.objects.filter(Q(age=q) | Q(phone__contains=q)).order_by('-created_at')
    else:
        all_editor_list = Editor.objects.all().order_by('-created_at')

    paginator = Paginator(all_editor_list, 4)
    page = request.GET.get('page')
    all_editor = paginator.get_page(page)

    return render(request, 'backend.html', {"editores": all_editor})


# Function to Add patient
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url = "login")
def add_editor(request):
    if request.method == 'POST':

        # Check if email exist in BD
        email = request.POST['email']
        phone = request.POST['phone']
        if Registered_Data.objects.filter(email=email).exists():
            messages.error(request, "Correo electrónico ya ha sido registrado en nuestra Base de Datos")
            return HttpResponseRedirect('/')
        elif Registered_Data.objects.filter(phone=phone).exists():
            messages.error(request, "Teléfono ya ha sido registrado en nuestra Base de Datos")
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
        return render(request, "edit.html", {"editor":editor})


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
@login_required(login_url = "login")
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
        return render(request, "edit_publication.html", {"musical_publication":musical_publication})


# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_musical_publication(request):
    if request.method == "POST":
        musical_publication = Musical_Publication.objects.get(id = request.POST.get('id'))
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
