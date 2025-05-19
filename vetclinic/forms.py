from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Pet
from captcha.fields import CaptchaField


class AppointmentRequestForm(forms.Form):
    pet_name = forms.CharField(max_length=50)
    species = forms.ChoiceField(choices=Pet.SPECIES_CHOICES)
    owner_name = forms.CharField(max_length=100)
    owner_email = forms.EmailField()
    owner_phone = forms.CharField(max_length=20)
    # TODO: Create varificatrion for preferred_date automatically
    preferred_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    captcha = CaptchaField()


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

    def save(self, commit=True):
        user = super().save(commit=False)
        random_password = get_random_string(8)
        user.set_password(random_password)
        user.is_staff = True
        self._generated_password = random_password
        if commit:
            user.save()
            self.save_m2m()
        return user

    def get_generated_password(self):
        return getattr(self, "_generated_password", None)
