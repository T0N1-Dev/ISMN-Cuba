from django.contrib import admin

from App.models import (Editor, Musical_Publication, Especialista, Registered_Data, Rango_Prefijo_Editor,
                        Rango_Prefijo_Publicacion, PrefijoEditor, PrefijoPublicacion, Solicitud)

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre no puede contener nada que no sea letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido no puede contener nada que no sea letras.")
        return last_name


class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            return not obj.is_superuser
    form = CustomUserAdminForm


class EditorInline(admin.StackedInline):
    model = Editor
    verbose_name_plural = "editores"


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'prefijo']
    search_fields = ['user', 'phone', 'prefijo']
    list_per_page = 8


class EspecialistaInline(admin.StackedInline):
    model = Especialista
    verbose_name_plural = "especialistas"


@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'directions']
    search_fields = ['user', 'phone', 'directions']
    list_per_page = 8


class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name', 'autor', 'editor', 'ismn', 'imagen', 'gender']
    search_fields = ['name', 'autor', 'editor', 'ismn', 'gender']
    list_per_page = 8


class Prefijo_Editor_Admin(admin.ModelAdmin):
    list_display = ['value', 'lote', 'rango']


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['editor', 'tipo', 'created_at', 'status']
    search_fields = ['editor', 'tipo', 'created_at', 'status']
    list_per_page = 8


admin.site.register(Registered_Data)
admin.site.register(Musical_Publication, Musical_Publication_Admin)
admin.site.register(Rango_Prefijo_Editor)
admin.site.register(Rango_Prefijo_Publicacion)
admin.site.register(PrefijoEditor, Prefijo_Editor_Admin)
admin.site.register(PrefijoPublicacion)
admin.site.register(Solicitud, SolicitudAdmin)
# Desregistras el UserAdmin predeterminado
admin.site.unregister(User)

# Registras tu UserAdmin personalizado
admin.site.register(User, CustomUserAdmin)
