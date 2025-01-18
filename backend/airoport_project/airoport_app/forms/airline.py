from django import forms
from django.forms.widgets import TextInput

from airoport_app.db_tools import add_airline, update_airline

# форма для добавления авикомпании 
class AirlineForm(forms.Form):
    airline_name = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Нзавние авиакомпании'}))

    def save(self, commit=True, *args, **kwargs):
        airline_name = self.cleaned_data['airline_name']
        add_airline(
            airline_name=airline_name,
        )


#форма для обновления авикомпании
class UpdateAirlineForm(forms.Form):
    old_airline_name = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Старое авиакомпании'}))
    new_airline_name = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Нзавние авиакомпании'}))

    def save(self, commit=True, *args, **kwargs):
        old_airline_name = self.cleaned_data['old_airline_name']
        new_airline_name = self.cleaned_data['new_airline_name']
        update_airline(
            airline_old_name=old_airline_name,
            airline_new_name=new_airline_name,
        )
        