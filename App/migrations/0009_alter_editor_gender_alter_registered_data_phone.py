# Generated by Django 4.2.2 on 2023-08-16 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_registered_data_delete_registered_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='gender',
            field=models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='registered_data',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
