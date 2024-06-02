from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

#
# @receiver(m2m_changed, sender=User.groups.through)
# def enforce_single_group_membership(sender, instance, action, **kwargs):
#     if action == 'pre_add':
#         # Los nombres de los grupos que deseas restringir
#         restricted_groups = {'Editores', 'Especialistas', 'Administrador'}
#
#         # Obtener los grupos actuales del usuario
#         user_groups = instance.groups.values_list('name', flat=True)
#         # Nuevos grupos a los que el usuario está intentando unirse
#         new_groups = Group.objects.filter(pk__in=kwargs.get('pk_set', []))
#         new_group_names = {group.name for group in new_groups}
#
#         # Verificar intersección entre los grupos restringidos y los actuales del usuario
#         if restricted_groups.intersection(user_groups) and restricted_groups.intersection(new_group_names) \
#                 or new_groups.count() != 1:
#             raise ValueError(
#                 "El usuario solo puede pertenecer a uno de los grupos: Editores, Especialistas, o Administrador.")