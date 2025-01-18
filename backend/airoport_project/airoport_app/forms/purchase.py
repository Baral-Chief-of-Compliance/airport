from django import forms
from django.forms.widgets import TextInput, NumberInput, CheckboxInput

from airoport_app.db_tools import make_purchase

# форма для осуществелния покупки билета
class BuyTicketForm(forms.Form):

    # данные пассажира
    surname_passenger = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Фамилия пассажира'}))
    name_passenger = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Имя пассажира'}))
    patronymic_passenger = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Отчество пассажира'}))

    phone_number_passenger = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder': 'Номер телефона пассажира'}))

    passenger_age = forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Возраст пассажира', 'min': 0}))

    passport_series_passenger = forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Серия паспорта'}))
    passport_number_passenger = forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Номер паспорта'}))

    # данные загран паспорта
    abroad_passport_series_passenger = forms.IntegerField(required=False, widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Серия загран паспорта'}))
    abroad_passport_number_passenger = forms.IntegerField(required=False, widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Номер загран паспорта'}))

    # данные для визы пассажира
    visa_validity_period = forms.IntegerField(required=False, widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Срок действия визы'}))
    visa_type = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Тип визы'}))
    visa_number_of_permitted_entries = forms.IntegerField(required=False, widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Кол-во разрешенных въездов визы'}))
    visa_number = forms.CharField(required=False, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Номер визы'}))

    # селект для кассира
    cashiers = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(
            attrs={'class': 'custom-select', 'id': 'cashiersSelect'},
        )
    )

    # поле для тарифа
    tarif_code = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'номер тарифа'}))

    # поля для доп платы за питомца
    extra_fee_for_dog = forms.DecimalField(required=False, widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена доп. платы за питомца', 'min': 0, 'step': 0.01}))

    #наличие багажа
    luggage_availability = forms.BooleanField(required=False, widget=CheckboxInput(attrs={'class':'form-control'}))

    #наличие питомца
    hand_luggage_availability = forms.BooleanField(required=False, widget=CheckboxInput(attrs={'class': 'form-control'}))

    #наличие ручной клади
    having_pet = forms.BooleanField(required=False, widget=CheckboxInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        cashiers_choise = kwargs.pop('cashiers')
        super().__init__(*args, **kwargs)
        self.fields['cashiers'].choices = cashiers_choise


    def save(self, commit=True, *args, **kwargs):
        flight_number = kwargs.pop('flight_number',None)
        ticket_number = kwargs.pop('ticket_number',None)
        make_purchase(
          surname_passenger=self.cleaned_data['surname_passenger'],
          name_passenger=self.cleaned_data['name_passenger'],
          patronymic_passenger=self.cleaned_data['patronymic_passenger'],
          phone_number_passenger=self.cleaned_data['phone_number_passenger'],
          passenger_age=self.cleaned_data['passenger_age'],
          passport_number_passenger=self.cleaned_data['passport_number_passenger'],
          passport_series_passenger=self.cleaned_data['passport_series_passenger'],
          abroad_passport_number_passenger=self.cleaned_data['abroad_passport_number_passenger'],
          abroad_passport_series_passenger=self.cleaned_data['abroad_passport_series_passenger'],
          visa_validity_period=self.cleaned_data['visa_validity_period'],
          visa_type=self.cleaned_data['visa_type'],
          visa_number_of_permitted_entries=self.cleaned_data['visa_number_of_permitted_entries'],
          visa_number=self.cleaned_data['visa_number'],
          cashier_id=self.cleaned_data['cashiers'],
          tarif_code=self.cleaned_data['tarif_code'],
          extra_fee_for_dog=self.cleaned_data['extra_fee_for_dog'],
          flight_number=flight_number,
          ticket_number=ticket_number,
          luggage_availability=self.cleaned_data['luggage_availability'],
          hand_luggage_availability=self.cleaned_data['hand_luggage_availability'],
          having_pet=self.cleaned_data['having_pet']
        )