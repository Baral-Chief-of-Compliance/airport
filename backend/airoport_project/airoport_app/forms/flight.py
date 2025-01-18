from django import forms
from django.forms.widgets import TextInput, NumberInput, DateTimeInput, CheckboxInput

from airoport_app.db_tools import add_flight, update_flight, add_ticket, update_flight_time

# форма для добавления полета
class FlightForm(forms.Form):
    flight_airline = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={'class': 'custom-select', 'id': 'airlineSelect'},
        )
    )
    flight_place_departure = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Место отправления'}))
    flight_place_destination = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Место назначения'}))
    flight_date_time=forms.DateTimeField(
        widget=DateTimeInput(
            attrs={
                'class':'form-control border-secondary',
                'placeholder': 'Дата и время вылета',
                'id': 'date-time-picker'
            }
        )
    )
    flight_passengers_count=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Кол-во пассажирова', 'min':0, 'max':999}))
    flight_number_economy_class=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Кол-во мест "эконом класса"', 'min':0, 'max':999}))
    flight_number_premium_economy_class=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Кол-во мест "эконом-премиум класса"', 'min':0, 'max':999}))
    flight_number_business_class=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Кол-во мест "бизнес класса"', 'min':0, 'max':999}))
    flight_number_first_class=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Кол-во мест "первого класс"', 'min':0, 'max':999}))

    flight_not_valid_until_day=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'id':'nvud', 'placeholder':'НДД (дней)', 'min':0, 'max':366}))
    flight_not_valid_after_day=forms.IntegerField(widget=NumberInput(attrs={'class':'form-control', 'id':'nvad', 'placeholder':'НДП (дней)', 'min':0, 'max':366}))

    flight_international=forms.BooleanField(
        required=False,
        widget=CheckboxInput(attrs={'class': 'form-control'})
        )
    
    flight_price_economy_class=forms.DecimalField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена за "эконом"', 'min': 0, 'step': 0.01}))
    flight_price_premium_economy_class=forms.DecimalField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена за "эконом-премиум"', 'min': 0, 'step': 0.01}))
    flight_price_business_class=forms.DecimalField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена за "бизнес"', 'min': 0, 'step': 0.01}))
    flight_price_first_class=forms.DecimalField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена за "первый класс"', 'min': 0, 'step': 0.01}))

    def __init__(self, *args, **kwargs):
        flight_airline_choises = kwargs.pop('flight_airline')
        super().__init__(*args, **kwargs)
        self.fields['flight_airline'].choices = flight_airline_choises

    def save(self, commit=True, *args, **kwargs):
        flight_passengers_count = self.cleaned_data['flight_passengers_count']
        flight_number_first_class = self.cleaned_data['flight_number_first_class']
        flight_number_business_class = self.cleaned_data['flight_number_business_class']
        flight_number_premium_economy_class = self.cleaned_data['flight_number_premium_economy_class']
        flight_number_economy_class = self.cleaned_data['flight_number_economy_class']
        
        flight_number = add_flight(
            flight_airline=self.cleaned_data['flight_airline'],
            flight_place_departure=self.cleaned_data['flight_place_departure'],
            flight_place_destination=self.cleaned_data['flight_place_destination'],
            flight_date=self.cleaned_data['flight_date_time'].date(),
            flight_time=self.cleaned_data['flight_date_time'].time(),
            flight_passengers_count=flight_passengers_count,
            flight_international=self.cleaned_data['flight_international']
        )

        difference_passengers_first_class: int = flight_passengers_count - flight_number_first_class
        difference_passengers_business_class: int = 0
        difference_passengers_premium_economy_class : int =0
        difference_passengers_economy_class : int = 0

        passengers_count_first_class: int = 0
        passengers_count_business_class: int = 0 
        passengers_count_premium_economy_class: int = 0
        passengers_count_economy_class: int = 0

        if difference_passengers_first_class > 0:
            passengers_count_first_class = flight_number_first_class
            difference_passengers_business_class = difference_passengers_first_class - flight_number_business_class

            if difference_passengers_business_class > 0:
                passengers_count_business_class = flight_number_business_class
                difference_passengers_premium_economy_class = difference_passengers_business_class - flight_number_premium_economy_class

                if difference_passengers_premium_economy_class > 0:
                    passengers_count_premium_economy_class = flight_number_premium_economy_class
                    difference_passengers_economy_class = difference_passengers_premium_economy_class - flight_number_economy_class

                    if difference_passengers_economy_class > 0:
                        passengers_count_economy_class = flight_number_economy_class
                    else:
                        passengers_count_economy_class = difference_passengers_premium_economy_class
                
                else:
                    passengers_count_premium_economy_class = difference_passengers_business_class
            else:
                passengers_count_business_class = difference_passengers_first_class
        else:
            passengers_count_first_class = flight_passengers_count


        ticket_index = 0

        for i in range(passengers_count_first_class):
            add_ticket(
                flight_number=flight_number,
                ticket_index=ticket_index,
                ticket_class='Первый класс',
                flight_date_time=self.cleaned_data['flight_date_time'].date(),
                flight_not_valid_after_day=self.cleaned_data['flight_not_valid_after_day'] ,
                flight_not_valid_until_day=self.cleaned_data['flight_not_valid_until_day'],
                ticket_price=self.cleaned_data['flight_price_first_class']
            )
            ticket_index += 1

        for i in range(passengers_count_business_class):
            add_ticket(
                flight_number=flight_number,
                ticket_index=ticket_index,
                ticket_class='Бизнес класс',
                flight_date_time=self.cleaned_data['flight_date_time'].date(),
                flight_not_valid_after_day=self.cleaned_data['flight_not_valid_after_day'] ,
                flight_not_valid_until_day=self.cleaned_data['flight_not_valid_until_day'],
                ticket_price=self.cleaned_data['flight_price_business_class']
            )
            ticket_index += 1   

        for i in range(passengers_count_premium_economy_class):
            add_ticket(
                flight_number=flight_number,
                ticket_index=ticket_index,
                ticket_class='Эконом-премиум класс',
                flight_date_time=self.cleaned_data['flight_date_time'].date(),
                flight_not_valid_after_day=self.cleaned_data['flight_not_valid_after_day'] ,
                flight_not_valid_until_day=self.cleaned_data['flight_not_valid_until_day'],
                ticket_price=self.cleaned_data['flight_price_premium_economy_class']
            )
            ticket_index += 1   

        for i in range(passengers_count_economy_class):
            add_ticket(
                flight_number=flight_number,
                ticket_index=ticket_index,
                ticket_class='Эконом класс',
                flight_date_time=self.cleaned_data['flight_date_time'].date(),
                flight_not_valid_after_day=self.cleaned_data['flight_not_valid_after_day'] ,
                flight_not_valid_until_day=self.cleaned_data['flight_not_valid_until_day'],
                ticket_price=self.cleaned_data['flight_price_economy_class']
            )
            ticket_index += 1 

# форма для обновления вылета
class UpdateFlightForm(forms.Form):
    flight_date_time=forms.DateTimeField(
        widget=DateTimeInput(
            attrs={
                'class':'form-control border-secondary',
                'placeholder': 'Дата и время вылета',
                'id': 'date-time-picker'
            }
        )
    )

    def save(self, commit=True, *args, **kwargs):
        flight_number = kwargs.pop('flight_number',None)
        update_flight_time(
            flight_number=flight_number,
            flight_date=self.cleaned_data['flight_date_time'].date(),
            flight_time=self.cleaned_data['flight_date_time'].time()
        )