from django.contrib.auth import login
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.shortcuts import redirect,render,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..models import User,Quiz,Vehicle,CarHistory
from ..forms import CustomerSignUpForm
from ..decorators import customer_required
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Avg, Count

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request,"Successfully signed up")
        return redirect('login')

@method_decorator([login_required,customer_required], name='dispatch')
class CustListView(ListView):
    model = Vehicle
    ordering = ('licenceplate',)
    context_object_name = 'vehicles'
    template_name = 'accounts/customer/quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.vehicles\
        .select_related('owner')
        return queryset




@method_decorator([login_required,customer_required], name='dispatch')
class VehicleCreateView(CreateView):
    model =  Vehicle
    context_object_name = 'vehicle'
    fields = ('car_make','car_model',)
    template_name = 'accounts/customer/vehicle_add_form.html'


    def form_valid(self, form):
        vehicle=form.save(commit=False)
        vehicle.owner=self.request.user
        vehicle.save()
        messages.success(self.request,"Vehicle updated with success")
        return redirect('customer:custdashboard')


def custdashboard(request):
        items = Vehicle.objects.all()
        return render(request,'accounts/customer/custdashboard.html',context={'items':items})



@method_decorator([login_required,customer_required],name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ('car_make','car_model',)
    context_object_name = 'vehicles'
    template_name = 'accounts/customer/vehicle_change_form.html'

    def form_valid(self, form):
        vehicle=form.save(commit=False)
        vehicle.owner=self.request.user
        vehicle.save()
        messages.success(self.request,"Vehicle updated with success")
        return redirect('customer:vehicle_change', vehicle.pk)

    def get_success_url(self):
        return reverse('customer:vehicle_change',kwargs={'pk':self.object.pk})


@method_decorator([login_required, customer_required], name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Vehicle
    context_object_name = 'vehicle'
    template_name = 'accounts/customer/vehicle_delete_form.html'
    success_url = reverse_lazy('customer:quiz_list')

    def delete(self, request, *args, **kwargs):
        vehicle= self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.vehicles





class HistoryCreateView(CreateView):
    model = CarHistory
    context_object_name = 'history'
    fields = ('service','service_date','mechanic_name','garage_location','New_Car_Part','Part_Cost','location','repair_done','service_cost')
    template_name = 'accounts/customer/history_add_form.html'



    def form_valid(self, form):
        history=form.save(commit=False)
        history.owner=self.request.user
        history.save()
        messages.success(self.request,'Repair updated with success')
        return redirect('customer:custdashboard')

@method_decorator([login_required,customer_required], name='dispatch')
class HistoryListView(ListView):
        model = CarHistory
        context_object_name = 'history'
        template_name = 'accounts/customer/history_list.html'


        def get_queryset(self):
            queryset=self.request.user.history\
                .select_related('owner')
            return queryset


@method_decorator([login_required,customer_required], name='dispatch')
class HistoryUpdateView(UpdateView):
    model = CarHistory
    context_object_name = 'history'
    fields = ('service','service_date','mechanic_name','garage_location','New_Car_Part','Part_Cost','location','repair_done','service_cost')
    template_name = 'accounts/customer/history_change_form.html'


    def form_valid(self,form):
        history=form.save(commit=False)
        history.owner=self.request.user
        history.save()
        messages.success(self.request,'History Update with success')
        return redirect('customer:history_change',history.pk)

    def get_success_url(self):
        return reverse('customer:history_change',kwargs={'pk':self.object.pk})


@method_decorator([login_required,customer_required], name='dispatch')
class HistoryDeleteView(DeleteView):
    model = CarHistory
    context_object_name = 'history'
    template_name = 'accounts/customer/history_delete_form.html'
    success_url = reverse_lazy('customer:history_list')

    def delete(self, request, *args, **kwargs):
        history = self.get_object()
        messages.success(request, 'Car repair was deleted with success!')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.history
