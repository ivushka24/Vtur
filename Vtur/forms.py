from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AddOrder(forms.Form):
    person_numbers = forms.IntegerField(min_value=1, label='Количество человек')
    contact_phone = forms.RegexField(regex=r'^\+375\d{9}$', label='Номер телефона', error_messages={'invalid':'Введите телефон в формате +375ххххххххх'})

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']





