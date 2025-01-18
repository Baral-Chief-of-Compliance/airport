from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm



#форма для авторизации пользователя
class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Логин'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Пароль'}))

    def confirm_login_allowed(self, user):
        return super().confirm_login_allowed(user)