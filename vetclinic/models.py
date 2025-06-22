from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('reptile', 'Reptile'),
        ('other', 'Other'),
    ]
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    name = models.CharField(max_length=50)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='unknown')
    date_of_birth = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return f"{self.name} ({self.species})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField()
    vet = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vet_appointments')
    assistant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assistant_appointments')
    services = models.ManyToManyField(Service, blank=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} on {self.date.strftime('%Y-%m-%d %H:%M')} with {self.vet.username}"


class PendingAppointmentRequest(models.Model):
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    owner_phone = models.CharField(max_length=20)
    pet_name = models.CharField(max_length=50)
    species = models.CharField(max_length=10, choices=Pet.SPECIES_CHOICES, default='unknown')
    vet = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_vet_appointments', null=True, blank=True)
    assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pending_assistant_appointments', null=True, blank=True)
    preferred_date = models.DateTimeField()
    description = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.pet_name} on {self.preferred_date.strftime('%Y-%m-%d %H:%M')}"


class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescriptions = models.TextField(blank=True)
    follow_up_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Record for {self.appointment.pet.name} on {self.appointment.date.strftime('%Y-%m-%d')}"


class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    issued_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Invoice #{self.id} for {self.appointment.pet.name}"

