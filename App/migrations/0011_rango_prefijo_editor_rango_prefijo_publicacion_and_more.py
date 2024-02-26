# Generated by Django 4.2.5 on 2024-02-26 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_alter_editor_type_alter_musical_publication_imagen_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rango_Prefijo_Editor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_inferior', models.PositiveSmallIntegerField()),
                ('rango_superior', models.PositiveSmallIntegerField()),
                ('tipo', models.CharField(choices=[('P-Medio', 'P-Medio'), ('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Menor', 'P-Menor'), ('P-Medio_Inferior', 'P-Medio_Inferior')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'rangos',
            },
        ),
        migrations.CreateModel(
            name='Rango_Prefijo_Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_superior', models.PositiveSmallIntegerField()),
                ('tipo', models.CharField(choices=[('P-Superior', 'P-Superior'), ('P-Inferior', 'P-Inferior'), ('P-Media_Inferior', 'P-Medio_Inferior'), ('P-Media', 'P-Medio'), ('P-Menor', 'P-Menor')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'rangos',
            },
        ),
        migrations.AlterField(
            model_name='editor',
            name='prefijo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='App.prefijoeditor'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='type',
            field=models.CharField(choices=[('Compañia', 'Compañia'), ('Independiente', 'Independiente')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='musical_publication',
            name='imagen',
            field=models.ImageField(default='default.jpg', upload_to='publications'),
        ),
        migrations.AlterField(
            model_name='prefijoeditor',
            name='rango',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.rango_prefijo_editor'),
        ),
        migrations.AlterField(
            model_name='prefijopublicacion',
            name='rango',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='App.rango_prefijo_publicacion'),
        ),
        migrations.DeleteModel(
            name='Rango_Prefijo',
        ),
    ]
