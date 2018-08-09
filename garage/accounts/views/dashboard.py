from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from ..decorators import customer_required
from ..models import Repair,Contact
from ..filters import  ContactFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class VehicleRepairListView(ListView):
        model = Repair
        repair = Repair.objects.all()
        repair.count()
        context_object_name = 'repair'
        template_name = 'accounts/reports/custdashboard_list.html'


@method_decorator([login_required,customer_required], name='dispatch')
class ContactCreateView(CreateView):
    model = Contact
    context_object_name = 'contact'
    fields = ('first_name','last_name','phone_number','group','image','file')
    template_name = 'accounts/dashboard/contact_add_form.html'



    def form_valid(self, form):
        repair=form.save(commit=False)
        repair.name=self.request.user
        repair.save()
        messages.success(self.request,'Contact created successfully')
        return redirect('customer:repair_list')


@method_decorator([login_required,customer_required], name='dispatch')
class ContactListView(ListView):
    model = Contact
    template_name = 'accounts/dashboard/contact_list.html'
    context_object_name = 'contact'
    paginate_by = 3
    queryset = Contact.objects.all()


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['contact']=ContactFilter(self.request.GET,queryset=self.get_queryset())
        return context



@method_decorator([login_required,customer_required], name='dispatch')
class ContactDetailView(DetailView):
    model = Contact
    context_object_name = 'contact'
    template_name = 'accounts/dashboard/contact_detail.html'


    # def get_context_data(self, **kwargs):
    #     context= super(ContactDetailView, self).get_context_data(**kwargs)
    #     context['contact'] =Contact.objects.filter().count()
    #
    #     return context
