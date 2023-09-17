from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Prevent duplicated emails
class Registered_Data(models.Model):
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"email: {self.email} \n phone: {self.phone}"


# ==========MODELS TO MY BUSINESS=========
class Editor(models.Model):
    COMPANY = 'C'
    INDEPENDENCY = 'I'

    TYPE = {
        (COMPANY, 'Compañia'),
        (INDEPENDENCY, 'Independiente'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)],
                                           null=True, blank=True)
    type = models.CharField(max_length=100, null=True, choices=TYPE)
    image_profile = models.ImageField(upload_to="profile", null=True, default="profile_default.png")
    note = models.TextField(blank=True)
    directions = models.CharField(max_length=150)
    id_tribute = models.PositiveBigIntegerField()
    state = models.BooleanField(default=True)


class Editor_Prefijo(models.Model):
    value = models.PositiveIntegerField()
    lot = models.CharField(max_length=7)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True)
    inferior_range = models.PositiveIntegerField()
    superior_range = models.PositiveIntegerField()


class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    image_profile = models.ImageField(upload_to="profile", null=True, default="profile_default.png")
    directions = models.CharField(max_length=150)


class Musical_Publication(models.Model):
    BOLERO = 'Bolero'
    POPULAR_BAILABLE = 'Popular Bailable'
    MAMBO = 'Mambo'
    CHACHACHA = 'ChaChaCha'
    RUMBA = 'Rumba'
    DANZON = 'Danzón'

    MUSICAL_GENDER = [
        (BOLERO, "Bolero"),
        (POPULAR_BAILABLE, "Popular Bailable"),
        (MAMBO, "Mambo"),
        (CHACHACHA, "ChaChaCha"),
        (RUMBA, "Rumba"),
        (DANZON, "Danzón"),
    ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    ismn = models.CharField(max_length=20, unique=True)
    letra = models.FileField(upload_to="publications/letters")
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", null=True, default="default.jpg")
    date_time = models.DateField()
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)


class Musical_Publication_Prefijo(models.Model):
    value = models.PositiveIntegerField()
    lot = models.CharField(max_length=7)
    musical_publication = models.OneToOneField(Musical_Publication, on_delete=models.CASCADE)
    inferior_range = models.PositiveIntegerField()
    superior_range = models.PositiveIntegerField()
