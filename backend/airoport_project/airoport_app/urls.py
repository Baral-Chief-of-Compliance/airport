from django.urls import path, include
from django.contrib.auth.views import LogoutView
import airoport_app.views as views

app_name = 'airoport_app'


urlpatterns = [
    path('', view=views.index, name='index'),
    path('login/', view=views.AuthenticationFromView.as_view(), name='login'),
    path('logout/', view=LogoutView.as_view(), name='logout'),
    #маршруты для кассиров
    path('cashiers/', view=views.ListCashiersView.as_view(), name='list_cashiers'),
    path('cashiers/add_cashier/', view=views.AddCashierFormView.as_view(), name='add_cashier'),
    path('cashiers/update_cashier/<int:cashier_id>/', view=views.UpdateCashierFormView.as_view(), name='update_cashier'),
    path('cashiers/delete_cashier/<int:cashier_id>/', view=views.delete_cashier_path, name='delete_cashier'),
    #маршруты для авиакомпаний
    path('airlines/', view=views.ListAirlineView.as_view(), name='list_airlines'),
    path('airlines/add_airline/', view=views.AddAirlineFormView.as_view(), name='add_airline'),
    path('airlines/update_airline/<str:airline_name>/', view=views.UpdateAirlineFormView.as_view(), name='update_airline'),
    path('airlines/delete_cashier/<str:airline_name>/', view=views.delete_airline_path, name='delete_airline'),
    # маршруты для вылетов
    path('flights/', view=views.ListFlightView.as_view(), name='list_flights'),
    path('flights/add_flight/', view=views.AddFlightFormView.as_view(), name='add_flight'),
    path('flights/update_flight/<str:flight_number>/', view=views.UpdateFlightFormView.as_view(), name='update_flight'),
    path('flights/delete_flight/<str:flight_number>/', view=views.delete_flight_path, name='delete_flight'),
    path('flights/cancel_flight/<str:flight_number>/', view=views.cancel_flight_path, name='cancel_flight'),
    # маршруты для тарифов
    path('tarifs/', view=views.ListTarifView.as_view(), name='list_tarifs'),
    path('airlines/<str:airline_name>/tarifs/', view=views.ListTariDefineAirlineView.as_view(), name='list_tarifs_airline'),
    path('airlines/<str:airline_name>/tarifs/add_tarif/', view=views.AddTarifFormView.as_view(), name='add_tarif'),
    path('airlines/<str:airline_name>/tarifs/update_tarif/<str:tarif_code>/', view=views.UpdateTarifFormView.as_view(), name='update_tarif'),
    path('airlines/<str:airline_name>/tarifs/delete_tarif/<str:tarif_code>/', view=views.delete_tarif_path, name='delete_tarif'),
    # билеты полета
    path('flights/<str:flight_number>/tickets/', view=views.ListTicketView.as_view(), name='flight_tickets_list'),
    # купить билет
    path('flights/<str:flight_number>/tickets/<str:ticket_number>/buy/', view=views.BuyTicketFormViews.as_view(), name='buy_ticket'),
    path('flights/<str:flight_number>/tickets/<str:ticket_number>/pass/', view=views.pass_ticket_path, name='pass_ticket'),
    #получить информацию о конкретном билете
    path('flights/<str:flight_number>/tickets/<str:ticket_number>/info/', view=views.InfoTicketView.as_view(), name='info_ticket'),
    path('flights/<str:flight_number>/tickets/<str:ticket_number>/print/', view=views.get_paper_version_check, name='print_ticket'),
]