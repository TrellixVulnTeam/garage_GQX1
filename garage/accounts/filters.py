from django import forms
from .models import User, MechProfile,ClientRepairs,Vehicle,Contact

import django_filters


class MechProfileFilter(django_filters.FilterSet):
    # garage_name = django_filters.CharFilter(lookup_expr='icontains')
    # name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MechProfile
        fields = ['garage_name', 'county', 'name',]

class RepairFilter(django_filters.FilterSet):
    class Meta:
        model= ClientRepairs
        fields=['name','car_model','license_plate','Issue','created_on']

class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model= Vehicle
        paginate_by= 3
        fields={
            'vehicle_name':['icontains'],
             'number_plate':['icontains'],
             'ownership':['icontains'],
            'status':['icontains'],
        }
class ContactFilter(django_filters.FilterSet):
    class Meta:
        model= Contact
        paginate_by= 3
        fields = ('first_name','last_name','phone_number','group',)
