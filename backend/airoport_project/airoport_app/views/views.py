from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from airoport_app.forms import AuthForm


LOGIN_URL = 'airoport_app:login'

#главная страница
def index(request):
    return render(
        request=request,
        template_name='index.html'
    )


#представление для авторизации
class AuthenticationFromView(LoginView):
    template_name = 'authentication.html'
    authentication_form=AuthForm
    next_page = 'airoport_app:list_flights'