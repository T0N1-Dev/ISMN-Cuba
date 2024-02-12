from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import os


# Prevent duplicated emails
class Registered_Data(models.Model):
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"email: {self.email} \n phone: {self.phone}"


# ==========MODELS TO MY BUSINESS==========

# Models to manage the prefix numbers
class Rango_Prefijo(models.Model):
    # NOTAS
    # Los Editores que publican más son los que se les asignan menores números en el prefijo y si publican menos
    # tendrán un prefijo mayor. Más info en http://127.0.0.1:8000/ayuda

    PUBLICADOR_SUPERIOR = "P-Superior"  # rango-inferior: 0 rango-superior: 99
    PUBLICADOR_MEDIO = "P-Medio"  # rango-inferior: 100 rango-superior: 999
    PUBLICADOR_MEDIO_INFERIOR = "P-Medio_Inferior"  # rango-inferior: 1000 rango-superior: 9999
    PUBLICADOR_INFERIOR = "P-Inferior"  # rango-inferior: 10000 rango-superior: 99999
    PUBLICADOR_MENOR = "P-Menor"  # rango-inferior: 100000 rango-superior: 999999

    TYPE = {
        (PUBLICADOR_SUPERIOR, "P-Superior"),
        (PUBLICADOR_MEDIO, "P-Medio"),
        (PUBLICADOR_MEDIO_INFERIOR, "P-Medio_Inferior"),
        (PUBLICADOR_INFERIOR, "P-Inferior"),
        (PUBLICADOR_MENOR, "P-Menor")
    }

    rango_inferior = models.PositiveSmallIntegerField()
    rango_superior = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TYPE, unique=True)

    class Meta:
        verbose_name_plural = "rangos"

    def __str__(self):
        return f'{self.tipo}'


class PrefijoEditor(models.Model):
    value = models.PositiveSmallIntegerField(unique=True)
    lote = models.CharField(max_length=7)
    rango = models.ForeignKey(Rango_Prefijo, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Prefijos_Editores"

    def __str__(self):
        return f'{self.value}'


class PrefijoPublicacion(models.Model):
    value = models.PositiveSmallIntegerField(unique=True)
    lote = models.CharField(max_length=7)
    rango = models.ForeignKey(Rango_Prefijo, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Publicaciones Prefijos"

    def __str__(self):
        return f'{self.value}'


# Modelos que representan a los actores del sistema
class Editor(models.Model):
    COMPANY_EDITOR = 'Compañia'
    EDITOR_INDEPENDIENTE = 'Independiente'

    TYPE = {
        (COMPANY_EDITOR, 'Compañia'),
        (EDITOR_INDEPENDIENTE, 'Independiente'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)],
                                           null=True, blank=True)
    prefijo = models.ForeignKey(PrefijoEditor, on_delete=models.PROTECT)
    type = models.CharField(max_length=100, null=True, choices=TYPE)
    image_profile = models.ImageField(upload_to="profile", null=True, default="profile_default.png")
    note = models.TextField(blank=True)
    directions = models.CharField(max_length=150)
    id_tribute = models.PositiveBigIntegerField()
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "editores"

    def __str__(self):
        return self.user.first_name


class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    image_profile = models.ImageField(upload_to="profile", null=True, default="profile_default.png")
    directions = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "especialistas"

    def __str__(self):
        return self.user.first_name


# Modelo que representa a cada publicación musical
class Musical_Publication(models.Model):
    BOLERO_GENDER = 'Bolero'
    POPULAR_BAILABLE_GENDER = 'Popular Bailable'
    MAMBO_GENDER = 'Mambo'
    CHACHACHA_GENDER = 'Chachacha'
    RUMBA_GENDER = 'Rumba'
    DANZON_GENDER = 'Danzón'

    MUSICAL_GENDER = [
        (BOLERO_GENDER, "BL"),
        (POPULAR_BAILABLE_GENDER, "PB"),
        (MAMBO_GENDER, "MB"),
        (CHACHACHA_GENDER, "CH"),
        (RUMBA_GENDER, "RB"),
        (DANZON_GENDER, "DZ"),
    ]

    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True, blank=True)
    prefijo = models.OneToOneField(PrefijoPublicacion, on_delete=models.PROTECT)
    ismn = models.CharField(max_length=20, unique=True)
    letra = models.FileField(upload_to="publications/letters")
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", null=True, default="default.jpg")
    date_time = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)

    class Meta:
        verbose_name_plural = "publicaciones"

    def __str__(self):
        return self.name

    def letra_base_name(self):
        rute = self.letra.path
        return os.path.basename(rute)

    def image_base_name(self):
        rute = self.imagen.path
        return os.path.basename(rute)


# Solicitudes
class Solicitud(models.Model):

    EDITOR_ADD_SOLIC = 'EADDS'
    ISMN_ADD_SOLIC = 'ISMNADDS'

    SOLICITUD_TYPE = {
        (EDITOR_ADD_SOLIC, "Solicitud-Inscripción"),
        (ISMN_ADD_SOLIC, "Solicitud-ISMN")
    }

    PENDIENTE = 'PEND'
    ATENDIDO = 'ATEND'

    ESTATUS = {
        (PENDIENTE, "Pendiente"),
        (ATENDIDO, "Atendido")
    }

    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=SOLICITUD_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ESTATUS)


    class Meta:
        verbose_name_plural = 'solicitudes'
