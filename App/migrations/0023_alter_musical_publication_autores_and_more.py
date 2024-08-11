# Generated by Django 5.0.4 on 2024-08-10 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0022_alter_rango_prefijo_editor_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musical_publication',
            name='autores',
            field=models.ManyToManyField(blank=True, null=True, to='App.autor'),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio', 'P-Medio'), ('P-Superior', 'P-Superior'), ('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Inferior', 'P-Inferior')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Inferior', 'P-Inferior'), ('P-Superior', 'P-Superior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Media', 'P-Medio')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tema',
            name='idioma',
            field=models.CharField(choices=[('EN', 'Inglés'), ('PO', 'Portugués'), ('RU', 'Ruso'), ('IT', 'Italiano'), ('FR', 'Francés'), ('AL', 'Alemán'), ('ES', 'Español')], max_length=50),
        ),
    ]
