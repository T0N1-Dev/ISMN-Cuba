# Generated by Django 4.2.2 on 2023-07-16 21:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_musical_publication_autor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('age', models.IntegerField(validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(18)])),
                ('gender', models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=100, null=True)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
        migrations.AlterField(
            model_name='musical_publication',
            name='gender',
            field=models.CharField(choices=[('Bolero', 'Bolero'), ('Popular Bailable', 'Popular Bailable'), ('Mambo', 'Mambo'), ('ChaChaCha', 'ChaChaCha'), ('Rumba', 'Rumba'), ('Danzón', 'Danzón')], max_length=100, null=True),
        ),
    ]
