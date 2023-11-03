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
    SUPERIOR = "Superior"
    MEDIO = "Medio"
    MEDIO_INFERIOR = "Medio Inferior"
    INFERIOR = "Inferior"

    TYPE = {
        (SUPERIOR, "Superior"),
        (MEDIO, "Medio"),
        (MEDIO_INFERIOR, "Medio Inferior"),
        (INFERIOR, "Inferior")
    }

    rango_inferior = models.PositiveSmallIntegerField()
    rango_superior = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=20, choices=TYPE, unique=True)

    class Meta:
        verbose_name_plural = "rangos"

    def __str__(self):
        return f'{self.tipo}'


class Prefijo(models.Model):
    EDITOR_PREFIJO = 'E'
    PUBLICACION_MUSICAL_PREFIJO = "PM"

    TYPE = {
        (EDITOR_PREFIJO, 'Editor'),
        (PUBLICACION_MUSICAL_PREFIJO, "Publicacion Musical")
    }

    value = models.PositiveSmallIntegerField()
    lote = models.CharField(max_length=7)
    tipo = models.CharField(max_length=20, choices=TYPE)
    rango = models.ForeignKey(Rango_Prefijo, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "prefijos"

    def __str__(self):
        return f'{self.value}'


# Modelos que representan a los actores del sistema
class Editor(models.Model):
    COMPANY_EDITOR = 'C'
    EDITOR_INDEPENDIENTE = 'I'

    TYPE = {
        (COMPANY_EDITOR, 'Compañia'),
        (EDITOR_INDEPENDIENTE, 'Independiente'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)],
                                           null=True, blank=True)
    prefijo = models.ForeignKey(Prefijo, on_delete=models.PROTECT)
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

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True, blank=True)
    prefijo = models.OneToOneField(Prefijo, on_delete=models.PROTECT)
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
