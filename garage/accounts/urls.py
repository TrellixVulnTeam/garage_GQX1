from django.conf.urls import url,include
from django.views.generic import TemplateView
from .views import customer,mechanic,accounts,reports,dashboard
from django_filters.views import FilterView
from .filters import MechProfileFilter,RepairFilter

urlpatterns = [

    url('accounts/signup/mechanic/', mechanic.MechanicSignUpView.as_view(), name='mechanic_signup'),
    url('accounts/signup/customer/', customer.CustomerSignUpView.as_view(), name='customer_signup'),
    url('accounts/signup/', accounts.SignUpView.as_view(), name='signup'),
    # url(r'^search/$', FilterView.as_view(filterset_class=MechProfileFilter,template_name='accounts/mechanic/mech_list.html'), name='search'),


    # url('pdf', accounts.GeneratePdf.as_view(), name='pdf'),
    url('^$', accounts.home, name='home'),




#####################################customer#############################################
    url('customer/', include(([
    url(r'homepage', customer.homepage, name='homepage'),

    url('vehicle_delete/(?P<pk>[0-9]+)',customer.VehicleDeleteView.as_view(),name='vehicle_delete'),
    url('vehicle/list', customer.VehicleListView.as_view(), name='vehicle_list'),
    url('vehicleupdate/(?P<pk>[0-9]+)',customer.VehicleUpdateView.as_view(),name='vehicle_change'),

    url('vehicle/add',customer.VehicleCreateView.as_view(),name='vehicle_add'),
    url('vehicle/details/(?P<pk>[0-9]+)',customer.VehicleDetailView.as_view(),name='vehicle_detail'),
    url('export/vehicle', customer.VehicleExport, name='vehicle_export'),

    url(r'^mech_list$', customer.MechListView.as_view(), name='mech_list'),
    url(r'^$', customer.review_list, name='review_list'),
    url(r'^review/user/(?P<username>\w+)/$', customer.user_review_list, name='user_review_list'),
    url(r'^recommendation/$', customer.user_recommendation_list, name='user_recommendation_list'),
    url(r'^mechanic_review/add/(?P<mechprofile_id>[0-9]+)/$', customer.add_review, name='add_review'),
    url('vehicle/issue/add',customer.VehicleRepairCreateView.as_view(),name='issue_add'),
    url('vehicle/repair/list',customer.VehicleRepairListView.as_view(),name='repair_list'),
    url('vehicle/repair/detail/(?P<pk>[0-9]+)',customer.VehicleRepairDetailView.as_view(),name='repair_detail'),
    url('repair_change/update/(?P<pk>[0-9]+)',customer.VehicleUpdateView.as_view(),name='repair_change'),
    url('repair_service/delete/(?P<pk>[0-9]+)',customer.VehicleDeleteView.as_view(),name='repair_delete'),




], 'accounts'), namespace='customer')),



##########################################mechanic#########################################
    url('mechanic/', include(([
    url(r'^dent_removal/list',mechanic.dentlist.as_view(),name='dent_list'),
    url(r'^car_spa/list',mechanic.carSpalist.as_view(),name='car_spa'),
    url(r'^interior/list',mechanic.interiorlist.as_view(),name='interior'),
    url(r'^general_service/list',mechanic.servicelist.as_view(),name='service'),
    url(r'^client_repair/create',mechanic.ClientCreateView.as_view(),name='client_create'),
    url('client_repair/list',mechanic.ClientListView.as_view(),name='client_list'),
    url('client_repair/delete/(?P<pk>[0-9]+)',mechanic.ClientDeleteView.as_view(),name='client_delete'),
    url('client_repair/update/(?P<pk>[0-9]+)',mechanic.ClientUpdateView.as_view(),name='client_update'),

    url('profileupdate/(?P<pk>[0-9]+)',mechanic.MechanicUpdateView.as_view(),name='profile_change'),
    url('profiledelete/(?P<pk>[0-9]+)',mechanic.MechanicDeleteView.as_view(),name='profile_delete'),
    #url(r'^profiledetail/(?P<pk>[0-9]+)/$', mechanic.MechanicDetailView.as_view(), name='profile_detail'),
    url('dashboard', mechanic.mechdashboard, name='mechdashboard'),
    url('list',mechanic.MechListView.as_view(),name='mech_list'),
    url(r'^profiledetail/(?P<mechprofile_id>[0-9]+)/$', mechanic.profile_detail, name='profile_detail'),
    url(r'profile/detail(?P<pk>[0-9]+)', mechanic.ProfileDetailView.as_view(), name='myprofile_detail'),
    #url(r'profile/detail(?P<pk>[0-9]+)', mechanic.ProfileListView.as_view(), name='myprofile_list'),



     # url('Profile/Add',mechanic.ProfileCreateView.as_view(),name='profile_add'),
    url(r'^mechanic_review/add/(?P<mechprofile_id>[0-9]+)/$', mechanic.add_review, name='add_review'),
], 'accounts'), namespace='mechanic')),

################################reports#####################################################
    url('reports/', include(([
    url('vehicle/list', reports.VehicleListView.as_view(), name='vehicle_list'),
    url('reportlist', reports.reportlist, name='report_list'),
    url('mydashboard', reports.DashboardListView.as_view(), name='custdashboard'),


    url('export/Vehicle', reports.VehicleListExport, name='vehicle_export'),

   # url('dashboard', reports.DashboardList.as_view(), name='dashboard_list'),

], 'reports'), namespace='reports')),

###############################################dashboard############################

    url('dashboard/', include(([

     url('vehiclerepair/list1',dashboard.VehicleRepairListView.as_view(),name='repair_list'),

     url(r'^contact/create',dashboard.ContactCreateView.as_view(),name='contact_create'),
     url(r'^contact/list',dashboard.ContactListView.as_view(),name='contact_list'),
     url('contact/detail/(?P<pk>[0-9]+)',dashboard.ContactDetailView.as_view(),name='contact_detail'),
], 'dashboard'), namespace='dashboard')),



]


url('ratings/', include(([


], 'accounts'), namespace='accounts')),
