from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
import datetime

from .views import LOGIN_URL
from airoport_app.forms import FlightForm, UpdateFlightForm
from airoport_app.db_tools import get_all_flights, get_one_flight, delete_flight, get_all_airlines_for_flight_form, cancel_flight


# добавление вылета
class AddFlightFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'flight/add_flight.html'
    form_class = FlightForm
    success_url = reverse_lazy('airoport_app:list_flights')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['flight_airline'] = get_all_airlines_for_flight_form()
        return kwargs
    

# список вылетов
class ListFlightView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'flight/list_flight.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flights'] = get_all_flights()
        return context
    

# обновление данных вылета
class UpdateFlightFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'flight/update_flight.html'
    form_class = UpdateFlightForm
    success_url = reverse_lazy('airoport_app:list_flights')

    def get_context_data(self, **kwargs):
        flight_number = self.kwargs['flight_number']
        flight = get_one_flight(flight_number)
        
        #преоброзование timedelta from mysql to time
        value = datetime.timedelta(0, 64800)
        time = (datetime.datetime.min + flight['flight_time']).time()

        self.initial['flight_date_time'] = datetime.datetime.combine(flight['flight_date'], time)
        self.initial['flight_passengers_count'] = flight['flight_passengers_count']

        context = super().get_context_data(**kwargs)
        context['flight'] = flight
        return context

    def form_valid(self, form):
        form.save(
            flight_number = self.kwargs['flight_number']
        )
        return super().form_valid(form)
    

# удаление полета
@login_required
def delete_flight_path(request, flight_number:str) -> HttpResponseRedirect or HttpResponseNotAllowed:
    if request.method == 'POST':
        delete_flight(flight_number)
        return HttpResponseRedirect(reverse_lazy('airoport_app:list_flights'))
    else:
        return HttpResponseNotAllowed('This method is not allowed')
    

# отмена полета
@login_required
def cancel_flight_path(request, flight_number:str) -> HttpResponseRedirect or HttpResponseNotAllowed:
    if request.method == 'POST':
        cancel_flight(flight_number)
        return HttpResponseRedirect(reverse_lazy('airoport_app:list_flights'))
    else:
        return HttpResponseNotAllowed('This method is not allowed')