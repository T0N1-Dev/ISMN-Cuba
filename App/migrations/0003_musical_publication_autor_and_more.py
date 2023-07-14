# Generated by Django 4.2.2 on 2023-07-12 20:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_musical_publication_alter_patient_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='musical_publication',
            name='autor',
            field=models.CharField(default=93248234, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='musical_publication',
            name='ismn',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(18)]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
