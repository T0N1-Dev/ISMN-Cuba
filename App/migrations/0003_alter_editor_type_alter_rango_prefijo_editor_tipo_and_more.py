# Generated by Django 5.0.4 on 2024-05-10 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_editor_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='type',
            field=models.CharField(choices=[('Compañia', 'Compañia'), ('Independiente', 'Independiente')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_editor',
            name='tipo',
            field=models.CharField(choices=[('P-Medio_Inferior', 'P-Medio_Inferior'), ('P-Superior', 'P-Superior'), ('P-Medio', 'P-Medio'), ('P-Inferior', 'P-Inferior'), ('P-Menor', 'P-Menor')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo_publicacion',
            name='tipo',
            field=models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Menor', 'P-Menor'), ('P-Media', 'P-Medio'), ('P-Media_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True),
        ),
    ]
