# -*- coding: utf-8 -*-
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, FileResponse, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from docxtpl import DocxTemplate, RichText


from .views import LOGIN_URL
# from airoport_app.forms import AirlineForm, UpdateAirlineForm
from airoport_app.db_tools import get_all_flight_tickets, get_one_flight, get_purchase_by_ticket_number, get_one_passenger, get_one_visa, get_one_tarif, get_one_ticket, get_one_cashier, pass_ticket


# список всех билетов конкретного полета
class ListTicketView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'ticket/list_tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = get_all_flight_tickets(
            flight_number=self.kwargs['flight_number']
        )
        context['flight'] = get_one_flight(flight_number=self.kwargs['flight_number'])
        return context
    

# ифнормация о конкретном билете
class InfoTicketView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'ticket/info_ticket.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = get_one_ticket(
            ticket_number=self.kwargs['ticket_number']
        )
        flight = get_one_flight(flight_number=self.kwargs['flight_number'])

        purchase = get_purchase_by_ticket_number(ticket_number=self.kwargs['ticket_number'])
        context['ticket'] = ticket
        context['flight'] = flight
        context['purchase'] = purchase
        context['tarif'] = get_one_tarif(tarif_code=ticket['tarif_code'])
        context['passenger'] = get_one_passenger(
            passport_number_passenger=purchase['passenger_number'],
            passport_series_passenger=purchase['passenger_series']
        )

        context['visa'] = False

        context['cashier'] = get_one_cashier(purchase['cashier_id'])

        if flight['flight_international_status']:
            context['visa'] = get_one_visa(visa_number=purchase['visa_number'])
            
        return context
    

# получить распечатку билета
@login_required
def get_paper_version_check(req, flight_number:str, ticket_number:str):
    if req.method == 'GET':
        data = {}

        ticket = get_one_ticket(
            ticket_number=ticket_number
        )
        flight = get_one_flight(flight_number=flight_number)
        purchase = get_purchase_by_ticket_number(ticket_number=ticket_number)
        tarif = get_one_tarif(tarif_code=ticket['tarif_code'])
        passenger = get_one_passenger(
            passport_number_passenger=purchase['passenger_number'],
            passport_series_passenger=purchase['passenger_series']
        )
        cashier = get_one_cashier(purchase['cashier_id'])

        data.update(ticket)
        data.update(flight)
        data.update(purchase)
        data.update(tarif)
        data.update(passenger)
        data.update(cashier)

        data['visa'] = False

        if flight['flight_international_status']:
            data.update(get_one_visa(visa_number=purchase['visa_number']))

        # работа с шаблоном чека
        template_filename = '/home/django-app/airoport_app/views/template.docx'

        tpl = DocxTemplate(template_filename)

        response =  HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response["Content-Disposition"] = f'filename="check_{ticket_number}.docx"'

        tpl.render(data)
        tpl.save(response)

        return response
    else:
        return HttpResponseNotAllowed('This method is not  allowed')
    
# сдать билеты
@login_required
def pass_ticket_path(request, flight_number:str,  ticket_number: str):
    if request.method == 'POST':
        pass_ticket(ticket_number=ticket_number)
        return HttpResponseRedirect(
            reverse_lazy(
                'airoport_app:flight_tickets_list',
                kwargs={
                    'flight_number':flight_number
                }
                )
            )
    else:
        return HttpResponseNotAllowed('This method is not allowed')