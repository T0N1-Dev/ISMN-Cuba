from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from App.forms import CustomUserAdminForm
from App.models import (Editor, Especialista, Rango_Prefijo_Editor,
                        Rango_Prefijo_Publicacion, Editorial)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not all(char.isalpha() for char in first_name):
            raise ValidationError("El nombre es incorrecto.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not all(char.isalpha() for char in last_name):
            raise ValidationError("El apellido es incorrecto.")

        return last_name

    def clean(self):
        cleaned_data = super().clean()
        groups = cleaned_data.get('groups', [])

        # Los nombres de los grupos que deseas restringir
        restricted_groups = {'Editores', 'Especialistas', 'Administrador'}

        # Obtener los nombres de los grupos seleccionados
        selected_group_names = set(group.name for group in groups)

        # Verificar intersección entre los grupos restringidos
        if len(selected_group_names.intersection(restricted_groups)) > 1:
            raise forms.ValidationError(
                "El usuario solo puede pertenecer a uno de los grupos: Editores, Especialistas, o Administrador."
            )

        return cleaned_data


class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    readonly_fields = ('last_login', 'date_joined')
    list_display = ['username', 'first_name', 'email', 'is_staff', 'is_active']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            return not obj

    def save_model(self, request, obj, form, change):
        if change:
            if obj == request.user:
                original_obj = User.objects.get(pk=obj.pk)
                if original_obj.is_superuser and not obj.is_superuser:
                    messages.error(request, _("No puedes deshabilitar tu propio permiso de superusuario."))
                    obj.is_superuser = True
                if original_obj.is_staff and not obj.is_staff:
                    messages.error(request, _("No puedes deshabilitar tu propio permiso de staff."))
                    obj.is_staff = True
                if original_obj.is_active and not obj.is_active:
                    messages.error(request, _("No puedes deshabilitar tu propio estado activo."))
                    obj.is_active = True

            groups = form.cleaned_data.get('groups', [])
            restricted_groups = {'Editores', 'Especialistas', 'Administrador'}
            selected_group_names = set(group.name for group in groups)

            if len(selected_group_names.intersection(restricted_groups)) > 1:
                messages.error(request,
                               "El usuario solo puede pertenecer a uno de los grupos: Editores, Especialistas, o Administrador.")
                return

        super().save_model(request, obj, form, change)


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
            raise ValidationError("El teléfono no puede tener más de 14 dígitos.")

        return phone

    def clean_id_tribute(self):
        id_tribute = self.cleaned_data.get('id_tribute')

        if len(str(id_tribute)) > 14:
            raise ValidationError("El ID Tributario no puede tener más de 14 dígitos.")

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


class CustomEditorialAdminForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not all(char.isdigit() or char in ['+', '-'] for char in phone):
            raise ValidationError("El teléfono solo puede contener números, '+' y '-'.")

        if len(phone) > 14:
            raise ValidationError("El teléfono no puede tener más de 14 dígitos.")

        return phone

    def clean_id_tribute(self):
        id_tribute = self.cleaned_data.get('id_tribute')

        if len(str(id_tribute)) > 14:
            raise ValidationError("El ID Tributario no puede tener más de 14 dígitos.")

        return id_tribute

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        if birthday:
            if birthday > timezone.now().date():
                raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")

            if birthday.year < 1900:
                raise ValidationError("La fecha de nacimiento no puede ser anterior a 1900.")

        return birthday

class EditorialAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'prefijo']
    search_fields = ['user__first_name', 'phone', 'prefijo']
    list_per_page = 8
    form = CustomEditorialAdminForm


class CustomEspecialistaAdminForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = '__all__'

    def clean_CI(self):
        CI = self.cleaned_data.get('CI')

        if len(str(CI)) != 11:
            raise ValidationError("El Carnet de Identidad debe tener 11 dígitos.")

        return CI


class EspecialistaInline(admin.StackedInline):
    model = Especialista
    verbose_name_plural = "especialistas"


@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'directions']
    search_fields = ['user__first_name', 'phone', 'directions']
    list_per_page = 8
    form = CustomEspecialistaAdminForm


admin.site.register(Rango_Prefijo_Editor)
admin.site.register(Rango_Prefijo_Publicacion)
# admin.site.register(Editor, EditorAdmin)
# Desregistras el UserAdmin predeterminado
admin.site.unregister(User)
# Registras tu UserAdmin personalizado
admin.site.register(User, CustomUserAdmin)
