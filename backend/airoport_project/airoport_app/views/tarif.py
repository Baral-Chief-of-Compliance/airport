from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from .views import LOGIN_URL
from airoport_app.forms import TarifForm, UpdateTarifForm
from airoport_app.db_tools import get_all_tarifs, get_all_tarifs_from_airline, get_one_tarif, delete_tarif  


# добавление тарифа
class AddTarifFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'tarif/add_tarif.html'
    form_class = TarifForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airline_name'] = self.kwargs['airline_name']
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.save(airline_name=context['airline_name'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'airoport_app:list_tarifs_airline', 
            kwargs={
                'airline_name':self.kwargs['airline_name']
                }
            )
    
        

# список всех тарифов
class ListTarifView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'tarif/list_tarif.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarifs'] = get_all_tarifs()
        return context
    

# список всех тарифов конкретной авикомпании
class ListTariDefineAirlineView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'tarif/list_tarif_define_airline.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airline_name'] = self.kwargs['airline_name']
        context['tarifs'] = get_all_tarifs_from_airline(airline=self.kwargs['airline_name'])
        return context
    

# форма для обновления авикомпании
class UpdateTarifFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'tarif/update_tarif.html'
    form_class = UpdateTarifForm

    def get_context_data(self, **kwargs):

        tarif_code = self.kwargs['tarif_code']
        airline_name = self.kwargs['airline_name']
        tarif = get_one_tarif(tarif_code)

        self.initial['name'] = tarif['name']
        self.initial['permissible_luggage_weight'] = tarif['permissible_luggage_weight']
        self.initial['permissible_weight_hand_luggage'] = tarif['permissible_weight_hand_luggage']
        self.initial['extra_fee_for_pet'] = tarif['extra_fee_for_pet']
        self.initial['possibility_of_changing_ticket'] = tarif['possibility_of_changing_ticket']
        self.initial['choice_of_location'] = tarif['choice_of_location']
        self.initial['possibility_of_return'] = tarif['possibility_of_return']
        self.initial['number_of_accrued_bonuses'] = tarif['number_of_accrued_bonuses']
        self.initial['possibility_of_upgrade'] = tarif['possibility_of_upgrade']
        self.initial['availability_of_open_departure_date'] = tarif['availability_of_open_departure_date']
        self.initial['priority_registration'] = tarif['priority_registration']
        self.initial['priority_screening'] = tarif['priority_screening']
        self.initial['priority_boarding'] = tarif['priority_boarding']
        self.initial['priority_baggage_handling'] = tarif['priority_baggage_handling']
        self.initial['tarif_code'] = tarif['tarif_code']
        self.initial['airline_name'] = tarif['airline_name']

        context = super().get_context_data(**kwargs)
        context['tarif'] = tarif
        context['airline_name'] = airline_name
        context['tarif_code'] = tarif_code
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        form.save(
            airline_name=context['airline_name'],
            tarif_code=context['tarif_code']
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'airoport_app:list_tarifs_airline', 
            kwargs={
                'airline_name':self.kwargs['airline_name']
                }
            )


# удаление тарифа
@login_required
def delete_tarif_path(request, airline_name:str, tarif_code: str) -> HttpResponseRedirect or HttpResponseNotAllowed:
    if request.method == 'POST':
        delete_tarif(tarif_code)
        return HttpResponseRedirect(
            reverse_lazy(
                'airoport_app:list_tarifs_airline',
                kwargs={
                    'airline_name': airline_name
                }
                )
            )
    else:
        return HttpResponseNotAllowed('This method is not allowed')