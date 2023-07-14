from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Patient(models.Model):

    GENDER = {
        ('F','F'),
        ('M', 'M'),
    }

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)])
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Musical_Publication(models.Model):

    MUSICAL_GENDER = [
        ("Bolero","Bolero"),
        ("Popular Bailable","Popular Bailable"),
        ("Mambo","Mambo"),
        ("ChaChaCha","ChaChaCha"),
        ("Rumba","Rumba"),
        ("Danzón","Danzón"),
    ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    ismn = models.CharField(max_length=20)
    letter_contain = models.TextField()
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", null=True, default="default.jpg")
    date_time = models.DateField()
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)


