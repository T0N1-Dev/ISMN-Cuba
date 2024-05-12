import datetime
from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import os
# Validate Dates
from django.db.models import Min, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.contrib.auth.models import User


def validate_date(value):
    if value > timezone.now().date() or value.year < 1900:
        raise ValidationError('Error en la fecha.')


def validate_image_extension(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError('Solo se permiten archivos con extensiones .jpg, .jpeg o .png')


def validate_phone(value):
    if not all(char.isdigit() or char in ['+', '-'] for char in value):
        raise ValidationError("El teléfono solo puede contener números, '+' y '-'.")



# Prevent duplicated emails
class Registered_Data(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    id_tribute = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"email: {self.email} \n phone: {self.phone}"


# ==========MODELS TO MY BUSINESS==========

# Models to manage the prefix numbers
class Rango_Prefijo_Editor(models.Model):
    # NOTAS
    # El número de prefijo de un Editor viene dado por la cantidad de publicaciones que genera por año,
    # los editores que publican más son los que se les asignan menores números en el prefijo y si publican menos
    # tendrán un prefijo mayor. Más info en http://127.0.0.1:8000/ayuda/Prefijo-Editor

    PUBLICADOR_SUPERIOR = "P-Superior"  # rango-inferior: 0 rango-superior: 99
    PUBLICADOR_MEDIO = "P-Medio"  # rango-inferior: 100 rango-superior: 999
    PUBLICADOR_MEDIO_INFERIOR = "P-Medio_Inferior"  # rango-inferior: 1000 rango-superior: 9999
    PUBLICADOR_INFERIOR = "P-Inferior"  # rango-inferior: 10000 rango-superior: 99999
    PUBLICADOR_MENOR = "P-Menor"  # rango-inferior: 100000 rango-superior: 999999

    TYPE = {
        (PUBLICADOR_SUPERIOR, "P-Superior"),
        (PUBLICADOR_MEDIO, "P-Medio"),
        (PUBLICADOR_MEDIO_INFERIOR, "P-Medio_Inferior"),
        (PUBLICADOR_INFERIOR, "P-Inferior"),
        (PUBLICADOR_MENOR, "P-Menor")
    }

    rango_inferior = models.PositiveIntegerField()
    rango_superior = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TYPE, unique=True)

    class Meta:
        verbose_name_plural = "Rangos-Editores"

    def __str__(self):
        return f'{self.tipo}'


class Rango_Prefijo_Publicacion(models.Model):
    # NOTAS
    # Por otra parte los prefijos de las publicaciones si siguen un orden ascendente.
    # Donde todas comienzan en 0 y terminan en su rango superior.
    # Más info en http://127.0.0.1:8000/ayuda/Prefijo-Publicaciones

    PUBLICACION_SUPERIOR = "P-Superior"  # rango-superior: 999999
    PUBLICACION_MEDIA = "P-Media"  # rango-superior: 99999
    PUBLICACION_MEDIA_INFERIOR = "P-Media_Inferior"  # rango-superior: 9999
    PUBLICACION_INFERIOR = "P-Inferior"  # rango-superior: 999
    PUBLICACION_MENOR = "P-Menor"  # rango-superior: 99

    TYPE = {
        (PUBLICACION_SUPERIOR, "P-Superior"),
        (PUBLICACION_MEDIA, "P-Medio"),
        (PUBLICACION_MEDIA_INFERIOR, "P-Medio_Inferior"),
        (PUBLICACION_INFERIOR, "P-Inferior"),
        (PUBLICACION_MENOR, "P-Menor")
    }

    rango_superior = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TYPE, unique=True)

    class Meta:
        verbose_name_plural = "Rango-Publicaciones"

    def __str__(self):
        return f'{self.tipo}'


class PrefijoEditor(models.Model):
    value = models.PositiveIntegerField(unique=True)
    lote = models.CharField(max_length=7)
    rango = models.ForeignKey(Rango_Prefijo_Editor, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Prefijos-Editores"

    def __str__(self):
        return f'{self.value}'


class PrefijoPublicacion(models.Model):
    value = models.PositiveIntegerField()
    lote = models.CharField(max_length=7)
    rango = models.ForeignKey(Rango_Prefijo_Publicacion, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Publicaciones Prefijos"

    def __str__(self):
        return f'{self.value}'


# Modelos que representan a los actores del sistema
class Editor(models.Model):
    COMPANY_EDITOR = 'Compañia'
    EDITOR_INDEPENDIENTE = 'Independiente'

    TYPE = {
        (COMPANY_EDITOR, 'Compañia'),
        (EDITOR_INDEPENDIENTE, 'Independiente'),
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=14, validators=[validate_phone])
    birthday = models.DateField(validators=[validate_date], blank=True, null=True)
    prefijo = models.OneToOneField(PrefijoEditor, on_delete=models.PROTECT)
    type = models.CharField(max_length=100, choices=TYPE)
    image_profile = models.ImageField(upload_to="profile", blank=True, default="profile_default.png",
                                      validators=[validate_image_extension])
    note = models.TextField(blank=True)
    directions = models.CharField(max_length=150)
    id_tribute = models.PositiveSmallIntegerField(unique=True)
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "editores"

    def __str__(self):
        return self.user.first_name

    def get_state_display(self):
        return 'Activo' if self.state else 'Inactivo'


class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, max_length=14, validators=[validate_phone])
    note = models.TextField(blank=True)
    image_profile = models.ImageField(upload_to="profile", blank=True, default="profile_default.png",
                                      validators=[validate_image_extension])
    directions = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "especialistas"

    def __str__(self):
        return self.user.first_name


# Modelo que representa a cada publicación musical
class Musical_Publication(models.Model):
    BOLERO_GENDER = 'Bolero'
    FUSION = 'Fusion'
    POPULAR_BAILABLE_GENDER = 'Popular Bailable'
    MAMBO_GENDER = 'Mambo'
    CHACHACHA_GENDER = 'Chachacha'
    RUMBA_GENDER = 'Rumba'
    DANZON_GENDER = 'Danzón'

    MUSICAL_GENDER = [
        (BOLERO_GENDER, "BL"),
        (FUSION, 'FS'),
        (POPULAR_BAILABLE_GENDER, "PB"),
        (MAMBO_GENDER, "MB"),
        (CHACHACHA_GENDER, "CH"),
        (RUMBA_GENDER, "RB"),
        (DANZON_GENDER, "DZ"),
    ]

    name = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True, blank=True)
    prefijo = models.OneToOneField(PrefijoPublicacion, on_delete=models.CASCADE)
    ismn = models.CharField(max_length=20, unique=True)
    barcode = models.ImageField(upload_to="publications/barcodes")
    letra = models.FileField(upload_to="publications/letters")
    description = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publications", blank=True, default="default.jpg")
    date_time = models.DateTimeField(validators=[validate_date])
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=100, null=True, choices=MUSICAL_GENDER)

    class Meta:
        verbose_name_plural = "publicaciones"

    def __str__(self):
        return self.name

    def letra_base_name(self):
        rute = self.letra.path
        return os.path.basename(rute)

    def barcode_base_name(self):
        rute = self.barcode.path
        return os.path.basename(rute)

    def image_base_name(self):
        rute = self.imagen.path
        return os.path.basename(rute)


# Solicitudes
class Solicitud(models.Model):
    EDITOR_ADD_SOLIC = 'Solicitud-Inscripción'
    ISMN_ADD_SOLIC = 'Solicitud-ISMN'

    SOLICITUD_TYPE = {
        (EDITOR_ADD_SOLIC, "Solicitud-Inscripción"),
        (ISMN_ADD_SOLIC, "Solicitud-ISMN")
    }

    PENDIENTE = 'Pendiente'
    ATENDIDO = 'Atendido'

    ESTATUS = {
        (PENDIENTE, "Pendiente"),
        (ATENDIDO, "Atendido")
    }

    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True)
    temporal = models.JSONField()
    tipo = models.CharField(max_length=50, choices=SOLICITUD_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ESTATUS)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'solicitudes'

    def __str__(self):
        return self.tipo

    # Retorna todas las solicitudes que han sido aceptadas hasta ahora
    @classmethod
    def return_accepted(cls):
        # Obtener la fecha mínima en la que se creó una solicitud
        fecha_minima = cls.objects.aggregate(Min('created_at'))['created_at__min']

        # Si no hay solicitudes, retornar un diccionario vacío
        if not fecha_minima:
            return {}

        # Obtener la fecha actual
        fecha_actual = timezone.now().date()

        # Truncar la fecha mínima para obtener solo la fecha (sin hora)
        fecha_minima = fecha_minima.date()

        # Inicializar el diccionario de resultados con todas las fechas desde la mínima hasta la actual
        resultados = {fecha_minima + datetime.timedelta(days=d): {'Solicitud-ISMN': 0, 'Solicitud-Inscripción': 0} for d
                      in range((fecha_actual - fecha_minima).days + 1)}

        # Contar las solicitudes por fecha y actualizar el diccionario de resultados
        solicitudes_por_fecha_tipo = cls.objects.filter(status='Atendido').order_by('created_at'). \
            annotate(fecha=TruncDate('created_at')).values('fecha', 'tipo').annotate(total=Count('id'))

        for solicitud in solicitudes_por_fecha_tipo:
            fecha = solicitud['fecha']
            tipo = solicitud['tipo']
            total = solicitud['total']
            if fecha in resultados:
                resultados[fecha][tipo] += total
        return resultados

    # Retorna todas las solicitudes que han sido eliminadas o rechazadas
    @classmethod
    def return_deleted(cls):
        return cls.objects.filter(deleted=True, status='Pendiente').order_by('deleted_at')

    # Retorna todas las solicitudes que no han sido rechazadas, es decir, las aceptadas y las pendientes
    @classmethod
    def return_active(cls):
        return cls.objects.filter(deleted=False).order_by('created_at')

    # Retorna las solicitudes rechazadas el último año
    @classmethod
    def solicitudes_eliminadas_ultimo_anio(cls):
        # Obtener la fecha actual y la fecha de hace un año
        fecha_actual = timezone.now()
        fecha_hace_un_anio = fecha_actual - timezone.timedelta(days=365)

        # Crear un diccionario para almacenar el recuento de solicitudes eliminadas por mes
        diccionario_solicitudes_eliminadas = {}

        # Llenar el diccionario con todos los meses del último año, inicializados a 0
        fecha_mes = fecha_hace_un_anio.replace(day=1)
        while fecha_mes <= fecha_actual:
            nombre_mes = fecha_mes.strftime('%B')
            diccionario_solicitudes_eliminadas[nombre_mes] = defaultdict(int)
            fecha_mes = fecha_mes + timezone.timedelta(days=31)

        # Obtener todas las solicitudes eliminadas en el último año
        solicitudes_eliminadas = cls.objects.filter(deleted=True, deleted_at__gte=fecha_hace_un_anio)

        # Iterar sobre todas las solicitudes eliminadas
        for solicitud in solicitudes_eliminadas:
            mes = solicitud.deleted_at.strftime('%B')
            tipo_solicitud = solicitud.tipo
            diccionario_solicitudes_eliminadas[mes][tipo_solicitud] += 1

        # Extraer el primer elemento
        primer_elemento = next(iter(diccionario_solicitudes_eliminadas.items()))

        # Eliminar el primer elemento del diccionario
        del diccionario_solicitudes_eliminadas[primer_elemento[0]]

        # Insertar el primer elemento al final
        diccionario_solicitudes_eliminadas[primer_elemento[0]] = primer_elemento[1]

        return diccionario_solicitudes_eliminadas


    # Retorna un diccionario con las solicitudes enviadas en cada fecha hasta el dia de hoy
    @classmethod
    def solicitudes_enviadas_total(cls):

        # Obtener la fecha actual
        fecha_actual = timezone.now().date()

        # Inicializar el diccionario de resultados con las últimas 30 fechas
        resultados = {}
        fecha_iter = fecha_actual
        for _ in range(30):
            resultados[fecha_iter] = {'Solicitud-Inscripción': 0, 'Solicitud-ISMN': 0}
            fecha_iter -= datetime.timedelta(days=1)

        # Contar las solicitudes por fecha y actualizar el diccionario de resultados
        solicitudes_por_fecha_tipo = cls.objects.annotate(fecha=TruncDate('created_at')).values('fecha',
                                                                                                'tipo').annotate(
            total=Count('id'))
        for solicitud in solicitudes_por_fecha_tipo:
            fecha = solicitud['fecha']
            tipo = solicitud['tipo']
            total = solicitud['total']
            if fecha in resultados:
                resultados[fecha][tipo] = total

        # Imprimir resultados
        resultados_descendente = dict(reversed(list(resultados.items())))
        return resultados_descendente

    # Retorna todas las solicitude pendientes
    @classmethod
    def filter_pending_not_deleted_ordered(cls):
        return cls.objects.filter(status='Pendiente', deleted=False).order_by('-created_at')

    # "Borrar"
    def soft_delete(self):
        if not self.deleted:
            self.deleted = True
            self.deleted_at = timezone.now()
