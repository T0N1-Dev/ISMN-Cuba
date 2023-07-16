from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from App.models import Patient, Musical_Publication
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator

# ================= FRONTEND SECTION =================
# Function to render the Home Page
def frontend(request):
    return render(request, "frontend.html")

# ================= BACKEND SECTION =================
# Function to render the Backend Page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url = "login")
def backend(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_patient_list = Patient.objects.filter(
            Q(name__icontains=q) | Q(email=q) | Q(gender=q) | Q(note=q)
        ).order_by('-created_at')
    else:
        all_patient_list = Patient.objects.all().order_by('-created_at')

    paginator = Paginator(all_patient_list, 4)
    page = request.GET.get('page')
    all_patient = paginator.get_page(page)

    return render(request, 'backend.html', {"patients":all_patient})

# Function to Add patient
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url = "login")
def add_patient(request):
    if request.method == 'POST':
        if request.POST.get('name') \
                and request.POST.get('phone') \
                and request.POST.get('email') \
                and request.POST.get('age') \
                and request.POST.get('gender') \
                or request.POST.get('note'):
            patient = Patient()
            patient.name = request.POST.get('name')
            patient.phone = request.POST.get('phone')
            patient.email = request.POST.get('email')
            patient.age = request.POST.get('age')
            patient.gender = request.POST.get('gender')
            patient.note = request.POST.get('note')
            patient.save()
            messages.success(request, "Editor added successfully !")
            return HttpResponseRedirect('/backend')
    else:
        return render(request, "add.html")


# Function to delete patient
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()
    messages.success(request, "Editor removed succesfully !")
    return HttpResponseRedirect('/backend')

# Function to access the patient individually
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if patient:
        return render(request, "edit.html", {"patient":patient})

# Function to edit the patients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def edit_patient(request):
    if request.method == "POST":
        patient = Patient.objects.get(id = request.POST.get('id'))
        if patient:
            patient.name = request.POST.get("name")
            patient.phone = request.POST.get("phone")
            patient.email = request.POST.get("email")
            patient.age = request.POST.get("age")
            patient.gender = request.POST.get("gender")
            patient.note = request.POST.get("note")
            patient.save()
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
