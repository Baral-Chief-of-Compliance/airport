from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from .views import LOGIN_URL
from airoport_app.forms import CashierForm, UpdateCashierForm
from airoport_app.db_tools import get_all_cashiers, get_one_cashier, delete_cashier


#добавление кассира
class AddCashierFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'cashier/add_cashier.html'
    form_class = CashierForm
    success_url = reverse_lazy('airoport_app:list_cashiers')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

#список кассиров
class ListCashiersView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = 'cashier/list_cashiers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashiers'] = get_all_cashiers()
        return context
    

#обновление данных кассира
class UpdateCashierFormView(LoginRequiredMixin, FormView):
    login_url = LOGIN_URL
    template_name = 'cashier/update_cashier.html'
    form_class = UpdateCashierForm
    success_url = reverse_lazy('airoport_app:list_cashiers')

    def get_context_data(self, **kwargs): 
        cashier_id = self.kwargs['cashier_id']
        cashier = get_one_cashier(cashier_id)
        context = super().get_context_data(**kwargs)
        context['cashier'] = cashier
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cashier_id = self.kwargs['cashier_id']
        cashier = get_one_cashier(cashier_id)

        kwargs['cashier_id'] = cashier_id
        kwargs['cashier_surname'] = cashier['cashier_surname']

        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

#удаление кассира
@login_required
def delete_cashier_path(request, cashier_id:int) -> HttpResponseRedirect or HttpResponseNotAllowed:
    if request.method == 'POST':
        delete_cashier(cashier_id)
        return HttpResponseRedirect(reverse_lazy('airoport_app:list_cashiers'))
    else:
        return HttpResponseNotAllowed('This method is not allowed')