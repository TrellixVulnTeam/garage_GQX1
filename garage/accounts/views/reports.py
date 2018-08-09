from ..models import ClientRepairs
from ..filters import RepairFilter
from ..resources import ClientResource,VehicleResource
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from ..decorators import customer_required
from ..models import User, Vehicle,Repair
from django.http import HttpResponse
from django.views import generic
from ..filters import  VehicleFilter


def reportlist(request):
    repair=ClientRepairs.objects.all()
    repair_filter=RepairFilter(request.GET,queryset=repair)
    return render(request,'accounts/reports/service_report.html',{'filter': repair_filter})


#
# class VehicleListExport(ListView):
#     model = Vehicle
#     template_name = 'accounts/reports/service_report.html'
#
#     def get_queryset(self):
#         vehicles = VehicleResource()
#         dataset = vehicles.export()
#         response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="vehiclelist.xls"'
#         return response




@method_decorator([login_required,customer_required], name='dispatch')
class DashboardListView(generic.ListView):
    model = Vehicle
    context_object_name = 'vehicles'
    template_name = 'accounts/customer/custdashboard_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super(DashboardListView, self).get_context_data(**kwargs)
    #     return context


    def get_context_data(self, **kwargs):
            context= super(DashboardListView, self).get_context_data(**kwargs)
            context['vehicles'] = Vehicle.objects.filter(name=self.request.user).count()
            context['user'] =Repair.objects.all().count()

            return context


@method_decorator([login_required,customer_required], name='dispatch')
class VehicleListView(ListView):
    model = Vehicle
    context_object_name = 'vehicles'
    template_name = 'accounts/reports/vehiclereport_list.html'
    queryset = Vehicle.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['vehicles']=VehicleFilter(self.request.GET,queryset=self.get_queryset())
        return context



    # def get_queryset(self):
    #     queryset = self.request.user.vehicles\
    #     .select_related('name')
    #     return queryset


def VehicleListExport(request):
     vehicles = VehicleResource()
     dataset = vehicles.export()
     vehicles = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
     vehicles['Content-Disposition'] = 'attachment; filename="vehiclelist.xls"'
     return vehicles
