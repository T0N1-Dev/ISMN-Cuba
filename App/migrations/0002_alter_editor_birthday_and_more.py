# Generated by Django 5.0.4 on 2024-05-10 15:24

import App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='birthday',
            field=models.DateField(blank=True, null=True, validators=[App.models.validate_date]),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Menor', 'P-Menor'), ('P-Medio', 'P-Medio'), ('P-Medio_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Menor', 'P-Menor'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='status',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Atendido', 'Atendido')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('Solicitud-Inscripción', 'Solicitud-Inscripción'), ('Solicitud-ISMN', 'Solicitud-ISMN')], max_length=50),
        ),
    ]
