from django import forms
from .models import User


class UserAdminForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        exclude = ('password_hash', 'last_visit', 'city')

