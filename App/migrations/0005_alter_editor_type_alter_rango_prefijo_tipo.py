# Generated by Django 4.2.5 on 2024-02-05 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_rango_prefijo_tipo_alter_solicitud_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='type',
            field=models.CharField(choices=[('Independiente', 'Independiente'), ('Compañia', 'Compañia')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rango_prefijo',
            name='tipo',
            field=models.CharField(choices=[('Medio', 'Medio'), ('Superior', 'Superior'), ('Inferior', 'Inferior'), ('Medio Inferior', 'Medio Inferior')], max_length=20, unique=True),
        ),
    ]
