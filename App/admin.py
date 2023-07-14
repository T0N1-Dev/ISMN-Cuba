from django.contrib import admin
from App.models import Patient, Musical_Publication

class PatientAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','gender','created_at']
    search_fields = ['name', 'phone', 'email', 'gender']
    list_per_page = 8

admin.site.register(Patient, PatientAdmin)
admin.site.register(Musical_Publication)
