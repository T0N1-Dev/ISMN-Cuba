from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Prevent duplicated emails
class Registered_Data(models.Model):
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email, self.phone


# ==========*MODELS TO CUSTOM USER*==========
class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get("is_staff") is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get("is_superuser") is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'),  max_length=250, unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="profile", null=True, default="profile_default.png")
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_specialist = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["user_name", "first_name"]

    def __str__(self):
        return self.user_name


# ==========MODELS TO MY BUSINESS=========
class Editor(models.Model, CustomUser):
    MASCULINO = 'M'
    FEMENINO = 'F'

    GENDER = {
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    }

    id = models.IntegerField(primary_key=True)
    age = models.IntegerField(validators=[MaxValueValidator(120), MinValueValidator(18)])
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    note = models.TextField(blank=True)




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
    ismn = models.CharField(max_length=20, unique=True)
    letter_contain = models.TextField()
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", null=True, default="default.jpg")
    date_time = models.DateField()
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)

