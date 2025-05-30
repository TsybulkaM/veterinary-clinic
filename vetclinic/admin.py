from django.contrib import admin
from .models import Owner, Pet, Appointment, Service, MedicalRecord, Invoice
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from .admin_dashboard import custom_admin_site
from . import models

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'phone')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'owner')
    search_fields = ('name', 'owner__first_name', 'owner__last_name')
    list_filter = ('species',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'vet', 'assistant', 'status')
    list_filter = ('status', 'date')
    search_fields = ('pet__name', 'vet__username', 'assistant__username')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vet":
            try:
                vet_group = Group.objects.get(name="Veterinarian")
                kwargs["queryset"] = vet_group.user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        if db_field.name == "assistant":
            try:
                assistant_group = Group.objects.get(name="Assistant")
                kwargs["queryset"] = assistant_group.user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis', 'follow_up_date')
    search_fields = ('appointment__pet__name', 'diagnosis')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'total', 'is_paid', 'issued_date')
    list_filter = ('is_paid',)


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'groups'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and hasattr(form, "get_generated_password"):
            password = form.get_generated_password()
            messages.success(request, f"Generated password for {obj.username}: {password}")

# All models registration
for model in models.__dict__.values():
    try:
        if hasattr(model, '_meta'):
            custom_admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

custom_admin_site.unregister(User)
custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(Group)
