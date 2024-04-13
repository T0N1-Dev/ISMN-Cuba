from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual', widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="Nueva Contraseña", widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña", widget=forms.PasswordInput
    )
