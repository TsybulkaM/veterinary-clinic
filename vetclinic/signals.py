from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from .models import (
    Owner, Pet, Appointment, Service,
    MedicalRecord, Invoice
)

@receiver(post_migrate)
def create_roles_permissions(sender, **kwargs):
    roles_permissions = {
        'Administrator': {
            'models': [Owner, Pet, Appointment, Service, MedicalRecord, Invoice],
            'permissions': ['add', 'change', 'delete', 'view']
        },
        'Veterinarian': {
            'models': [Pet, Appointment, MedicalRecord],
            'permissions': ['add', 'change', 'view']
        },
        'Assistant': {
            'models': [Appointment, MedicalRecord],
            'permissions': ['view']
        },
        'Receptionist': {
            'models': [Owner, Pet, Appointment],
            'permissions': ['add', 'change', 'view']
        },
        'Accountant': {
            'models': [Invoice],
            'permissions': ['add', 'change', 'view']
        },
    }

    for role, config in roles_permissions.items():
        group, _ = Group.objects.get_or_create(name=role)
        permissions = []
        for model in config['models']:
            content_type = ContentType.objects.get_for_model(model)
            for perm in config['permissions']:
                codename = f"{perm}_{model._meta.model_name}"
                try:
                    permission = Permission.objects.get(
                        codename=codename,
                        content_type=content_type
                    )
                    permissions.append(permission)
                except Permission.DoesNotExist:
                    continue
        group.permissions.set(permissions)