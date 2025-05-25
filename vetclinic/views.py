from django.shortcuts import render

# vetclinic/views.py
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'vetclinic/homePage.html')

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
