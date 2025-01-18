from django import forms
from django.forms.widgets import TextInput, NumberInput

from airoport_app.db_tools import add_cashier, update_cashier


# форма для добавления кассира
class CashierForm(forms.Form):
    cashier_surname = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Фамилия кассира'}))

    def save(self, commit=True, *args, **kwargs):
        cashier_surname = self.cleaned_data['cashier_surname']
        add_cashier(surname=cashier_surname)


# форма для обновленя кассира
class UpdateCashierForm(forms.Form):
    cashier_id = forms.IntegerField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder':'Номер кассира'}))
    cashier_surname = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Фамилия кассира'}))

    def __init__(self, *args, **kwargs):
        cashier_id = kwargs.pop('cashier_id')
        cashier_surname = kwargs.pop('cashier_surname')
        super().__init__(*args, **kwargs)

        self.fields['cashier_id'].initial  = cashier_id
        self.fields['cashier_surname'].initial  = cashier_surname


    def save(self, commit=True, *args, **kwargs):
        cashier_surname = self.cleaned_data['cashier_surname']
        cashier_id = self.cleaned_data['cashier_id']
        update_cashier(id=cashier_id, surname=cashier_surname)
        

