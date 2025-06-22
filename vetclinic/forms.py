from django import forms
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from captcha.fields import CaptchaField


class AppointmentRequestForm(forms.Form):
    # Form fields should use forms.* not models.*
    pet_name = forms.CharField(max_length=50)
    owner_name = forms.CharField(max_length=100)
    owner_email = forms.EmailField()
    owner_phone = forms.CharField(max_length=20)
    preferred_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data['preferred_date']
        today = date.today()

        if isinstance(preferred_date, datetime):
            preferred_date = preferred_date.date()

        if preferred_date < today:
            raise ValidationError("Appointment date cannot be in the past.")

        return preferred_date


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