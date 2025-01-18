from django import forms
from django.forms.widgets import TextInput, NumberInput, CheckboxInput

from airoport_app.db_tools import add_tarif, update_tarif


# форма для добавления тарифа
class TarifForm(forms.Form):
    name=forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Название тарифа'}))
    permissible_luggage_weight=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Допустимый вес багажа(кг)', 'min':0, 'step': 0.01}))
    permissible_weight_hand_luggage=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Допустимый вес ручной клади(кг)', 'min':0, 'step': 0.01}))
    extra_fee_for_pet=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Доп.плата за питомца'}), required=False)
    possibility_of_changing_ticket=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность изменения билета'}), required=False)
    choice_of_location=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Выбор места'}), required=False)
    possibility_of_return=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность возврата'}), required=False)
    number_of_accrued_bonuses=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Кол-во начисления бонусов', 'min':0}))
    possibility_of_upgrade=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность повышения класса'}), required=False)
    availability_of_open_departure_date=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Наличие открытой даты вылета'}), required=False)
    priority_registration=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетная регистрация'}), required=False)
    priority_screening=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетный досмотр'}), required=False)
    priority_boarding=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетная посадка'}), required=False)
    priority_baggage_handling=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетное обслуживание багажа'}), required=False)
    # airline_name=forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Название авиакомпании'}))

    def save(self, commit=True, *args, **kwargs):
        airline_name = kwargs.pop('airline_name',None)
        add_tarif(
            name=self.cleaned_data['name'],
            permissible_luggage_weight=self.cleaned_data['permissible_luggage_weight'],
            permissible_weight_hand_luggage=self.cleaned_data['permissible_weight_hand_luggage'],
            extra_fee_for_pet=self.cleaned_data['extra_fee_for_pet'],
            possibility_of_changing_ticket=self.cleaned_data['possibility_of_changing_ticket'],
            choice_of_location=self.cleaned_data['choice_of_location'],
            possibility_of_return=self.cleaned_data['possibility_of_return'],
            number_of_accrued_bonuses=self.cleaned_data['number_of_accrued_bonuses'],
            possibility_of_upgrade=self.cleaned_data['possibility_of_upgrade'],
            availability_of_open_departure_date=self.cleaned_data['availability_of_open_departure_date'],
            priority_registration=self.cleaned_data['priority_registration'],
            priority_screening=self.cleaned_data['priority_screening'],
            priority_boarding=self.cleaned_data['priority_boarding'],
            priority_baggage_handling=self.cleaned_data['priority_baggage_handling'],
            airline_name=airline_name
        )

# форма для обновления тарифа
class UpdateTarifForm(forms.Form):
    name=forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Название тарифа'}))
    permissible_luggage_weight=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Допустимый вес багажа(кг)', 'min':0, 'step': 0.01}))
    permissible_weight_hand_luggage=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Допустимый вес ручной клади(кг)', 'min':0, 'step': 0.01}))
    extra_fee_for_pet=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Доп.плата за питомца'}), required=False)
    possibility_of_changing_ticket=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность изменения билета'}), required=False)
    choice_of_location=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Выбор места'}), required=False)
    possibility_of_return=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность возврата'}), required=False)
    number_of_accrued_bonuses=forms.FloatField(widget=NumberInput(attrs={'class':'form-control','placeholder':'Кол-во начисления бонусов', 'min':0}))
    possibility_of_upgrade=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Возможность повышения класса'}), required=False)
    availability_of_open_departure_date=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Наличие открытой даты вылета'}), required=False)
    priority_registration=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетная регистрация'}), required=False)
    priority_screening=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетный досмотр'}), required=False)
    priority_boarding=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетная посадка'}), required=False)
    priority_baggage_handling=forms.BooleanField(widget=CheckboxInput(attrs={'class':'form-control','placeholder':'Приоритетное обслуживание багажа'}), required=False)

    def save(self, commit=True, *args, **kwargs):
        airline_name = kwargs.pop('airline_name',None)
        tarif_code = kwargs.pop('tarif_code', None)
        update_tarif(
            name=self.cleaned_data['name'],
            permissible_luggage_weight=self.cleaned_data['permissible_luggage_weight'],
            permissible_weight_hand_luggage=self.cleaned_data['permissible_weight_hand_luggage'],
            extra_fee_for_pet=self.cleaned_data['extra_fee_for_pet'],
            possibility_of_changing_ticket=self.cleaned_data['possibility_of_changing_ticket'],
            choice_of_location=self.cleaned_data['choice_of_location'],
            possibility_of_return=self.cleaned_data['possibility_of_return'],
            number_of_accrued_bonuses=self.cleaned_data['number_of_accrued_bonuses'],
            possibility_of_upgrade=self.cleaned_data['possibility_of_upgrade'],
            availability_of_open_departure_date=self.cleaned_data['availability_of_open_departure_date'],
            priority_registration=self.cleaned_data['priority_registration'],
            priority_screening=self.cleaned_data['priority_screening'],
            priority_boarding=self.cleaned_data['priority_boarding'],
            priority_baggage_handling=self.cleaned_data['priority_baggage_handling'],
            tarif_code=tarif_code,
            airline_name=airline_name
        )