from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Prevent duplicated emails
class Registered_Data(models.Model):
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email, self.phone

class Editor(models.Model):

    FEMENINO = 'F'
    MASCULINO = 'M'

    GENDER = {
        (FEMENINO,'Femenino'),
        (MASCULINO, 'Masculino'),
    }

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    age = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)])
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Musical_Publication(models.Model):

    BOLERO = 'Bolero'
    POPULAR_BAILABLE = 'Popular Bailable'
    MAMBO = 'Mambo'
    CHACHACHA = 'ChaChaCha'
    RUMBA = 'Rumba'
    DANZON = 'Danzón'
    MUSICAL_GENDER = [
        (BOLERO,"Bolero"),
        (POPULAR_BAILABLE,"Popular Bailable"),
        (MAMBO,"Mambo"),
        (CHACHACHA,"ChaChaCha"),
        (RUMBA,"Rumba"),
        (DANZON,"Danzón"),
    ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    ismn = models.CharField(max_length=20, unique=True)
    letter_contain = models.TextField()
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", null=True, default="default.jpg")
    date_time = models.DateField()
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)


