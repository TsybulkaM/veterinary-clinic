from django.contrib import admin, messages
from .models import Owner, Pet, Appointment, PendingAppointmentRequest, Service, MedicalRecord, Invoice
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect


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


@admin.register(PendingAppointmentRequest)
class PendingAppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'owner_name', 'owner_email', 'owner_phone', 'preferred_date')
    search_fields = ('owner_name', 'owner_email', 'pet_name')
    list_filter = ('is_processed', 'preferred_date')
    actions = ['process_requests']

    class Media:
        js = ('admin/js/set_default_action.js',)

    def changelist_view(self, request, extra_context=None):
        if 'is_processed__exact' not in request.GET:
            query = request.GET.copy()
            query['is_processed__exact'] = '0'
            return redirect(f"{request.path}?{query.urlencode()}")
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description="Verify and process selected requests")
    def process_requests(self, request, queryset):
        for pending_request in queryset:
            if pending_request.is_processed:
                continue

            owner, created = Owner.objects.get_or_create(
                phone=pending_request.owner_phone,
                defaults={
                    "first_name": pending_request.owner_name.split()[0],
                    "last_name": ' '.join(pending_request.owner_name.split()[1:]),
                    "email": pending_request.owner_email,
                }
            )

            pet, _ = Pet.objects.get_or_create(
                name=pending_request.pet_name,
                owner=owner,
                species=pending_request.species,
            )

            appointment = Appointment.objects.create(
                pet=pet,
                date=pending_request.preferred_date,
                #TODO: Create varificatrion for free vet and assistant
                vet=pending_request.vet,
                assistant=pending_request.assistant,
                status='scheduled',
            )

            pending_request.is_processed = True
            pending_request.save()

        self.message_user(request, "Selected requests have been processed successfully.")


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


# main actions

admin.site.site_header = "VetClinic Management"
admin.site.site_title = "VetClinic Admin"
admin.site.index_title = "Welcome to VetClinic Administration"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
