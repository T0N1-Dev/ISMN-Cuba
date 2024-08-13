from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, re_path
from django.views.static import serve

from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('createsuperuser/', views.create_super_user),
    path('admin/', admin.site.urls),
    path('salvasBD/', views.backup_database, name='salvasBD'),
    path('restaurarBD/', views.restore_database, name='restoreBD'),
    # Path to render the Homepage
    path('', views.frontend, name="frontend"),
    # Path Login/Logout/Register
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    # Reset Password
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Edit profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # Register User
    path('get-municipios/', views.get_municipios, name='get_municipios'),
    path('crear_autor/', views.crear_autor, name='crear_autor'),
    path('register_autor_editor/', views.register_autor_editor, name='register_autor_editor'),
    path('register_editorial/', views.register_editorial, name='register_editorial'),
    # Email Confirmation
    path('email_confirmation/', views.email_confirmation, name='email_confirmation'),
    # ===============
    # BACKEND SECTION
    # ===============
    # Path to access the backend page
    path('backend/<str:order>', views.backend_editores, name="backend_editores"),
    path('backend_publicaciones/<str:order>', views.backend_publicaciones, name="backend_publicaciones"),
    path('backend_solicitudes/<str:order>', views.backend_solicitudes, name="backend_solicitudes"),
    path('backend_editoriales/<str:order>', views.backend_editoriales, name="backend_editoriales"),
    # Path to accept an inscription application
    path('accept_inscription/<str:solicitud_id>', views.accept_inscription, name="accept_inscription"),
    # Path to accept an ismn application
    path('accept_ismn_application/<str:solicitud_id>', views.accept_ismn_solicitud, name="accept_ismn_application"),
    # Path to add an editor
    path('add_editor/', views.add_editor, name="add_editor"),
    # Path to add an editor
    path('add_editorial/', views.add_editorial, name="add_editorial"),
    # Path to delete an editor
    path('delete_editor/<str:editor_id>', views.delete_editor, name="delete_editor"),
    # Path to delete an editorial
    path('delete_editorial/<str:editorial_id>', views.delete_editorial, name="delete_editorial"),
    # Path to access the editor individualy
    path('editor/<str:editor_id>', views.editor, name="editor"),
    # Path to edit the editor
    path('edit_editor/', views.edit_editor, name="edit_editor"),
    # Path to access the editor individualy
    path('editorial/<str:editorial_id>', views.editorial, name="editorial"),
    # Path to edit the editor
    path('edit_editorial/', views.edit_editorial, name="edit_editorial"),
    # Path to access the musical colections
    path('musical_colections/', views.musical_colections_list, name="musical_colections"),
    # Path to add a musical publication
    path('add_musical_publicaton/', views.add_musical_publication, name="add_musical_publicaction"),
    # Path to access the muscial publication individually
    path('musical_publication/<str:musical_publication_id>', views.musical_publication, name="musical_publication"),
    # Path to edit the musical publication
    path('edit_musical_publication/', views.edit_musical_publication, name="edit_musical_publication"),
    # Path to delete a Musical_Publication
    path('delete_musical_publication/<str:musical_publication_id>', views.delete_musical_publication, name="delete_musical_publication"),
    # Path to delete a Solicitud
    path('delete_solicitud/<str:solicitud_id>', views.delete_solicitud, name="delete_solicitud"),
    # Path to send an ISMN-application
    path('solicitud-ismn/', views.solicitud_ismn, name="solicitud-ismn"),

    # ========================== EXPORT DOCUMENTS ==========================
    # Path to export a single musical publication
    path('export_musical_publication/<str:musical_publication_id>', views.export_musical_publication, name="export_publication"),
    # Tables
    path('export_publications_list/', views.export_publications_list, name='export_publications_list'),
    path('export_editores_list/', views.export_editores_list, name='export_editores_list'),
    path('export_solicitudes_list/', views.export_solicitudes_list, name='export_solicitudes_list'),
    # Statistics
    path('export_statistics_solicitud', views.export_statistics_solicitud, name='export_statistics_solicitud'),

    # ========================== SEND EMAIL ==========================
    # Path to send confirmation-code
    path('send_code_confirmation', views.send_code_confirmation, name="home"),
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
