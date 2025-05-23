import bcrypt
from django import forms
from .models import User


class AvtomatAdminForm(forms.ModelForm):

    def clean_rro_id(self):
        rro_id = self.cleaned_data.get('rro_id')
        if rro_id and not rro_id.isdigit():
            raise forms.ValidationError('Invalid Characters')
        return rro_id

    def clean_security_state(self):
        security_id = self.cleaned_data.get('security_id')
        security_state = self.cleaned_data.get('security_state')
        if security_id and not security_state:
            raise forms.ValidationError('Check Security State! SecurityID is not empty!')
        if not security_id and security_state in (1, 2):
            raise forms.ValidationError('Check Security State! SecurityID is empty!')
        return security_state

    def clean_price_for_app(self):
        price_for_app = self.cleaned_data.get('price_for_app')
        if price_for_app is None or price_for_app <= 0:
            self.instance.visible_in_app = False
        return price_for_app

    def clean(self):
        cleaned_data = super().clean()
        house_db = self.instance.house
        house_form = cleaned_data.get('house')
        if house_db and house_db != house_form:
            cleaned_data['longitude'] = None
            cleaned_data['latitude'] = None

        visible_in_app = cleaned_data.get('visible_in_app', self.instance.visible_in_app)
        price_for_app = cleaned_data.get('price_for_app', self.instance.price_for_app)

        if visible_in_app and (price_for_app is None or price_for_app <= 0):
            raise forms.ValidationError('Check Price for App! It should be > 0!')

        return cleaned_data


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
