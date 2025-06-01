from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentRequestForm
from .models import PendingAppointmentRequest

# vetclinic/views.py
from django.shortcuts import render

# Create your views here.
def home(request):
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

def appointment(request):
    return render(request, 'vetclinic/appointment.html')

def location(request):
    return render(request, 'vetclinic/location.html')

def about_view(request):
    return render(request, 'vetclinic/about.html')

def contact_view(request): # <--- ADD THIS FUNCTION (or ensure it's there)
    return render(request, 'vetclinic/contact.html')

def reviews(request):
    return render(request, 'vetclinic/reviews.html')

def shop(request):
    return  render(request,'vetclinic/shop.html' )
