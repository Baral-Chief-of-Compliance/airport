# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from .views import LOGIN_URL
from airoport_app.forms import AirlineForm, UpdateAirlineForm
from airoport_app.db_tools import get_all_airlines, get_one_airline, delete_airline


# добавление авикомпании
class AddAirlineFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'airline/add_airline.html'
    form_class = AirlineForm
    success_url = reverse_lazy('airoport_app:list_airlines')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

# список авикомпаний
class ListAirlineView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'airline/list_airlines.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airlines'] = get_all_airlines()
        return context
    

# обновление данных авикомпании
class UpdateAirlineFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'airline/update_airline.html'
    form_class = UpdateAirlineForm
    success_url = reverse_lazy('airoport_app:list_airlines')

    def get_context_data(self, **kwargs):

        airline_name = self.kwargs['airline_name']
        airline = get_one_airline(airline_name)

        self.initial['old_airline_name'] = airline['airline_name']
        self.initial['new_airline_name'] = airline['airline_name']

        context = super().get_context_data(**kwargs)
        context['airline'] = airline
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

# удаление авикомпании
@login_required
def delete_airline_path(request, airline_name:str) -> HttpResponseRedirect or HttpResponseNotAllowed:
    if request.method == 'POST':
        delete_airline(airline_name)
        return HttpResponseRedirect(reverse_lazy('airoport_app:list_airlines'))
    else:
        return HttpResponseNotAllowed('This method is not allowed')