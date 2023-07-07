from django.db import models

class Patient(models.Model):

    GENDER = {
        ('F','F'),
        ('M', 'M'),
    }

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

