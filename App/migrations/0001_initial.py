# Generated by Django 4.2.5 on 2024-01-26 23:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('phone', models.CharField(max_length=20)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(18)])),
                ('type', models.CharField(choices=[('C', 'Compañia'), ('I', 'Independiente')], max_length=100, null=True)),
                ('image_profile', models.ImageField(default='profile_default.png', null=True, upload_to='profile')),
                ('note', models.TextField(blank=True)),
                ('directions', models.CharField(max_length=150)),
                ('id_tribute', models.PositiveBigIntegerField()),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'editores',
            },
        ),
        migrations.CreateModel(
            name='Rango_Prefijo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_inferior', models.PositiveSmallIntegerField()),
                ('rango_superior', models.PositiveSmallIntegerField()),
                ('tipo', models.CharField(choices=[('Superior', 'Superior'), ('Medio', 'Medio'), ('Medio Inferior', 'Medio Inferior'), ('Inferior', 'Inferior')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'rangos',
            },
        ),
        migrations.CreateModel(
            name='Registered_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=40)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('EADDS', 'Solicitud-Inscripción'), ('ISMNADDS', 'Solicitud-ISMN')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PEND', 'Pendiente'), ('ATEND', 'Atendido')], max_length=50)),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.editor')),
            ],
            options={
                'verbose_name_plural': 'solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Prefijo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField()),
                ('lote', models.CharField(max_length=7)),
                ('tipo', models.CharField(choices=[('E', 'Editor'), ('PM', 'Publicacion Musical')], max_length=20)),
                ('rango', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.rango_prefijo')),
            ],
            options={
                'verbose_name_plural': 'prefijos',
            },
        ),
        migrations.CreateModel(
            name='Musical_Publication',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('autor', models.CharField(max_length=100)),
                ('ismn', models.CharField(max_length=20, unique=True)),
                ('letra', models.FileField(upload_to='publications/letters')),
                ('description', models.TextField(blank=True)),
                ('imagen', models.ImageField(default='default.jpg', null=True, upload_to='publications')),
                ('date_time', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('Bolero', 'BL'), ('Popular Bailable', 'PB'), ('Mambo', 'MB'), ('Chachacha', 'CH'), ('Rumba', 'RB'), ('Danzón', 'DZ')], max_length=100, null=True)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.editor')),
                ('prefijo', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.prefijo')),
            ],
            options={
                'verbose_name_plural': 'publicaciones',
            },
        ),
        migrations.CreateModel(
            name='Especialista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('note', models.TextField(blank=True)),
                ('image_profile', models.ImageField(default='profile_default.png', null=True, upload_to='profile')),
                ('directions', models.CharField(max_length=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'especialistas',
            },
        ),
        migrations.AddField(
            model_name='editor',
            name='prefijo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.prefijo'),
        ),
        migrations.AddField(
            model_name='editor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
