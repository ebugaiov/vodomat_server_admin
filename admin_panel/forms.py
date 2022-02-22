import bcrypt
from django import forms
from .models import User


class UserAdminForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        exclude = ('password_hash', 'last_visit', 'city')

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            password_bin = password.encode('utf-8')
            hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
            return password, hashed.decode('utf-8')
        else:
            return '', ''

    def clean(self):
        cleaned_data = super().clean()
        password, password_hash = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords are not equal')
        if password and len(password) < 4:
            raise forms.ValidationError('Password is too short')
        if self.instance.id is None and not password:
            raise forms.ValidationError('Password is required')
        cleaned_data['password_hash'] = password_hash
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        password_hash = self.cleaned_data['password_hash']
        if password_hash:
            instance.password_hash = password_hash
        if commit:
            instance.save()
        return instance
