from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


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


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Nombre', validators=[RegexValidator(r'^[a-zA-Z]*$', 'Solo se permiten letras.')])
    last_name = forms.CharField(label='Apellidos', validators=[RegexValidator(r'^[a-zA-Z]*$', 'Solo se permiten letras.')])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = "Las contraseñas no se almacenan en bruto, así que no hay manera de ver la " \
                                            "contraseña del usuario, pero se puede cambiar la contraseña mediante " \
                                            "<a href='/change_password/'>este enlace</a>."
