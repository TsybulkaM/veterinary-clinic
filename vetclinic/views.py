from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentRequestForm
from .models import PendingAppointmentRequest
from django.shortcuts import render
from datetime import date


def home(request):
    today = date.today().strftime('%Y-%m-%d')
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
                species='unknown',
            )
            messages.success(request, "Your appointment request has been submitted successfully. We'll contact you shortly.")
            return redirect('homePage')
    else:
        form = AppointmentRequestForm()

    if 'preferred_date' in form.fields:
        form.fields['preferred_date'].widget.attrs['min'] = today

    return render(request, 'vetclinic/homePage.html', {'form': form, 'today': today})

def appointment(request):
    today = date.today().strftime('%Y-%m-%d')
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
                species='unknown',
            )
            messages.success(request, "Your appointment request has been submitted successfully. We'll contact you shortly.")
            return redirect('homePage')
    else:
        form = AppointmentRequestForm()

    if 'preferred_date' in form.fields:
        form.fields['preferred_date'].widget.attrs['min'] = today

    return render(request, 'vetclinic/appointment.html', {'form': form, 'today': today})

def location(request):
    return render(request, 'vetclinic/location.html')

def about_view(request):
    return render(request, 'vetclinic/about.html')

def contact_view(request): # <--- ADD THIS FUNCTION (or ensure it's there)
    return render(request, 'vetclinic/contact.html')

def reviews(request):
    return render(request, 'vetclinic/reviews.html')

def shop(request):
    return render(request, 'vetclinic/shop.html')

def cart(request):
    return render(request, 'vetclinic/cart.html')