from  .models import Vehicle,MechProfile
import django_filters
from django import forms
class VehicleFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MechProfile
        fields = ['name',]
