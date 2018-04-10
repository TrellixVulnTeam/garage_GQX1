from django.conf.urls import url,include
from django.views.generic import TemplateView
from .views import customer,mechanic,accounts


urlpatterns = [

    url('accounts/signup/mechanic/', mechanic.MechanicSignUpView.as_view(), name='mechanic_signup'),
    url('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    url('accounts/signup/', accounts.SignUpView.as_view(), name='signup'),


    # url('pdf', accounts.GeneratePdf.as_view(), name='pdf'),
    url('^$', accounts.home, name='home'),




    url('customer/', include(([
    url('vehicle_delete/(?P<pk>[0-9]+)',customer.VehicleDeleteView.as_view(),name='vehicle_delete'),
    url('dashboard', customer.custdashboard, name='custdashboard'),
    url('list', customer.CustListView.as_view(), name='quiz_list'),
    url('vehicleupdate/(?P<pk>[0-9]+)',customer.VehicleUpdateView.as_view(),name='vehicle_change'),
    url('vehicle/add',customer.VehicleCreateView.as_view(),name='vehicle_add'),
    url('history/add',customer.HistoryCreateView.as_view(),name='history_add'),
    url('carhistory',customer.HistoryListView.as_view(),name='history_list'),
    url('historyupdate/(?P<pk>[0-9]+)',customer.HistoryUpdateView.as_view(),name='history_change'),
    url('historydelete/(?P<pk>[0-9]+)',customer.HistoryDeleteView.as_view(),name='history_delete'),
], 'accounts'), namespace='customer')),


    url('ratings/', include(([
    url('add', accounts.RateCreateView.as_view(),name='rate_add'),
    url('list',accounts.RateListView.as_view(),name='rate_list'),

], 'accounts'), namespace='accounts')),






    url('mechanic/', include(([
    url('profileupdate/(?P<pk>[0-9]+)',mechanic.MechanicUpdateView.as_view(),name='profile_change'),
    url('profiledelete/(?P<pk>[0-9]+)',mechanic.MechanicDeleteView.as_view(),name='profile_delete'),
    url('dashboard', mechanic.mechdashboard, name='mechdashboard'),
    url('list',mechanic.MechListView.as_view(),name='profile_list'),

     url('Profile/Add',mechanic.ProfileCreateView.as_view(),name='profile_add'),

      ], 'accounts'), namespace='mechanic')),




]
