from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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
