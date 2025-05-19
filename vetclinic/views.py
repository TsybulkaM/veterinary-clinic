from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentRequestForm
from .models import PendingAppointmentRequest


def home_page(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            PendingAppointmentRequest.objects.create(
                pet_name=form.cleaned_data['pet_name'],
                owner_name=form.cleaned_data['owner_name'],
                owner_email=form.cleaned_data['owner_email'],
                owner_phone=form.cleaned_data['owner_phone'],
                preferred_date=form.cleaned_data['preferred_date'],
                description=form.cleaned_data['description'],
            )
            messages.success(request, "Your request has been sent. An administrator will contact you to confirm.")
            return redirect('home_page')
    else:
        form = AppointmentRequestForm()
    return render(request, 'vetclinic/homePage.html', {'form': form})