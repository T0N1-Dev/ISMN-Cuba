from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from App.models import (Editor, Especialista, Registered_Data, Rango_Prefijo_Editor,
                        Rango_Prefijo_Publicacion)

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


class CustomEditorAdminForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not all(char.isdigit() or char in ['+', '-'] for char in phone):
            raise ValidationError("El teléfono solo puede contener números, '+' y '-'.")

        if len(phone) > 14:
            raise ValidationError("El teléfono no puede tener más de 14 caracteres.")

        return phone

    def clean_id_tribute(self):
        id_tribute = self.cleaned_data.get('id_tribute')

        if len(str(id_tribute)) > 14:
            raise ValidationError("El ID Tributario no puede tener más de 14 caracteres.")

        return id_tribute

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if birthday:
            if birthday > timezone.now().date():
                raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")

            if birthday.year < 1900:
                raise ValidationError("La fecha de nacimiento no puede ser anterior a 1900.")

        return birthday


class EditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'prefijo']
    search_fields = ['user__first_name', 'phone', 'prefijo']
    list_per_page = 8
    form = CustomEditorAdminForm


class EspecialistaInline(admin.StackedInline):
    model = Especialista
    verbose_name_plural = "especialistas"


@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'directions']
    search_fields = ['user__first_name', 'phone', 'directions']
    list_per_page = 8


admin.site.register(Registered_Data)
admin.site.register(Rango_Prefijo_Editor)
admin.site.register(Rango_Prefijo_Publicacion)
admin.site.register(Editor, EditorAdmin)
# Desregistras el UserAdmin predeterminado
admin.site.unregister(User)

# Registras tu UserAdmin personalizado
admin.site.register(User, CustomUserAdmin)
