from django.contrib import admin
from django.urls import path, include
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path to render the Homepage
    path('',views.frontend, name="frontend"),
    # Path Login/Logout
    path('/login/', include('django.contrib.auth.urls'), name='login'),
    # ===============
    # BACKEND SECTION
    # ===============
    # Path to access the backend page
    path('backend/',views.backend, name="backend"),
    # Path to add patient
    path('add_patient/',views.add_patient, name="add_patient"),
    # Path to delete patient
    path('delete_patient/<str:patient_id>', views.delete_patient, name="delete_patient"),
    # Path to access the patient individualy
    path('patient/<str:patient_id>', views.patient, name="patient"),
    # Path to edit the patient
    path('edit_patient/', views.edit_patient, name="edit_patient"),
    # Path to access the musical colections
    path('musical_colections/', views.musical_colections_list, name="musical_colections")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)