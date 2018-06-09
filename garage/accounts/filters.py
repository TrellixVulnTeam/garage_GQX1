from  .models import Vehicle
import django_filters
from django import forms
class VehicleFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Vehicle
        fields = ['name', 'make',]
