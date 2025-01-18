from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
import datetime


from .views import LOGIN_URL
from airoport_app.forms import BuyTicketForm
from airoport_app.db_tools import get_one_flight, get_one_ticket, get_all_tarifs_from_airline, get_all_cashiers_for_purchase_form


# покупка билета
class BuyTicketFormViews(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'purchase/buy_ticket.html'
    form_class = BuyTicketForm
    success_url = reverse_lazy('airoport_app:list_tickets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight_number = self.kwargs['flight_number']
        ticket_number = self.kwargs['ticket_number']
        flight = get_one_flight(flight_number=flight_number)
        
        context['flight_number'] = flight_number
        context['ticket_number'] = ticket_number
        context['flight'] = flight
        context['ticket'] = get_one_ticket(ticket_number=ticket_number)
        context['tarifs'] = get_all_tarifs_from_airline(airline=flight['flight_airline'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cashiers'] = get_all_cashiers_for_purchase_form()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        form.save(
            flight_number = context['flight_number'], 
            ticket_number = context['ticket_number']
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'airoport_app:flight_tickets_list',  
            kwargs={
                'flight_number': self.kwargs['flight_number']
            }
            )