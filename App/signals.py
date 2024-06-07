from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PrefijoEditor


@receiver(post_save, sender=PrefijoEditor)
def alert_near_limit(sender, instance, **kwargs):
    rango = instance.rango
    if instance.value >= rango.rango_superior * 0.9:
        print("Alerta: El valor de PrefijoEditor está cerca del 90% del rango superior permitido.")