import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

django.setup()

from App.models import Solicitud
from datetime import datetime, timedelta


fechas = []
editor = Solicitud.objects.all()[1].editor
temporal = {}
tipo = ['Solicitud-Inscripción', 'Solicitud-ISMN']
for dia in range(5, 31):
    fechas.append(datetime(2024, 4, dia))

status = 'Atendido'
contador = 0

for fecha in fechas:
    for r in range(random.choice([4, 3, 1, 0])):
        solicitud = Solicitud()
        solicitud.editor = editor
        solicitud.temporal = temporal
        solicitud.tipo = tipo[contador]
        if contador:
            contador -= 1
        else:
            contador += 1
        solicitud.status = status
        solicitud.save()
        solicitud.created_at = fecha
        solicitud.save()


