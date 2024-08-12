from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

try:
    # Reemplaza estos valores con los detalles de tu superusuario
    User.objects.create_superuser(
        username='tu_usuario',
        email='tu_correo@example.com',
        password='tu_contraseña'
    )
    print("Superusuario creado exitosamente.")
except IntegrityError:
    print("El superusuario ya existe.")