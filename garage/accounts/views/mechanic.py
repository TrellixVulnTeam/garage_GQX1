from django.contrib.auth import login
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.shortcuts import redirect,render,reverse
from django.contrib import  messages
from ..models import User,MechProfile,Review,ClientRepairs
from ..forms import MechanicSignUpForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import mechanic_required,customer_required
from django.urls import reverse_lazy

from ..forms import ReviewForm
import  datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from ..suggestions import update_clusters
from ..filters import VehicleFilter

def mechdashboard(request):
    items = MechProfile.objects.all()
    return render(request,'accounts/mechanic/mechdashboard.html',context={'items':items})

def search(request):
    user_list = MechProfile.objects.all()
    user_filter = VehicleFilter(request.GET, queryset=user_list)
    return render(request, 'accounts/mechanic/interior_list.html', {'filter': user_filter})

class MechanicSignUpView(CreateView):
    model = User
    form_class = MechanicSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mechanic'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request,"Successfully signed up,continue to login")
        return redirect('login')

@method_decorator([login_required,mechanic_required], name='dispatch')
class ProfileCreateView(CreateView):
    model = MechProfile
    context_object_name = 'mechprofile'
    fields = ('garage_name','county','desc','image','town','estate','dental_removal')
    template_name = 'accounts/mechanic/profile_add_form.html'

    def form_valid(self, form):
        mechprofile=form.save(commit=False)
        mechprofile.owner=self.request.user
        mechprofile.save()
        messages.success(self.request,'Profile Created with success')
        return redirect('mechanic:mechdashboard')


@method_decorator([login_required,mechanic_required],name='dispatch')
class MechanicUpdateView(UpdateView):
    model =  MechProfile
    fields = ('garage_name','county','desc','image','town','estate','dental_removal')
    context_object_name = 'mechprofile'
    template_name = 'accounts/mechanic/profile_change_form.html'

    def form_valid(self, form):
        mechprofile=form.save(commit=False)
        mechprofile.owner=self.request.user
        mechprofile.save()
        messages.success(self.request,'Profile Update with success')
        return redirect('mechanic:profile_change', mechprofile.pk)

    def get_success_url(self):
        return reverse('mechanic:profile_change',kwargs={'pk':self.object.pk})

class MechanicDeleteView(DeleteView):
    model = MechProfile
    context_object_name = 'mechprofile'
    template_name = 'accounts/mechanic/profile_delete_form.html'
    success_url = reverse_lazy('mechanic:profile_list')

    def delete(self, request, *args, **kwargs):
        profile = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.mechprofile

@method_decorator([login_required,customer_required], name='dispatch')
class dentlist(ListView):
    model = MechProfile
    context_object_name = 'dental_removal'
    template_name = 'accounts/mechanic/dent_list.html'
    paginate_by = 5


    def get_queryset(self):
        return MechProfile.objects.filter(dental_removal=True)

@method_decorator([login_required,customer_required], name='dispatch')
class interiorlist(ListView):
    model = MechProfile
    context_object_name = 'interior'
    template_name = 'accounts/mechanic/interior_list.html'
    paginate_by = 5

    def get_queryset(self):
        return MechProfile.objects.filter(interior_detailing=True)

@method_decorator([login_required,customer_required], name='dispatch')
class servicelist(ListView):
    model = MechProfile
    context_object_name = 'service'
    template_name = 'accounts/mechanic/service_list.html'
    paginate_by = 5

    def get_queryset(self):
        return MechProfile.objects.filter(general_service=True)

@method_decorator([login_required,customer_required], name='dispatch')
class carSpalist(ListView):
    model = MechProfile
    context_object_name = 'car_spa'
    template_name = 'accounts/mechanic/car_spa_list.html'
    paginate_by = 5

    def get_queryset(self):
        return MechProfile.objects.filter(car_spa=True)

@method_decorator([login_required,customer_required], name='dispatch')
class MechListView(ListView):
    model = MechProfile
    # ordering = ('user_name', )
    context_object_name = 'mechprofile'
    template_name = 'accounts/mechanic/mech_list.html'

    def get_queryset(self):
        queryset = self.request.user.mechprofile\
        .select_related('name')
        return queryset

@method_decorator([login_required,mechanic_required], name='dispatch')
class ClientListView(ListView):
    model = ClientRepairs
    # ordering = ('user_name', )
    context_object_name = 'client'
    template_name = 'accounts/mechanic/client_repair_list.html'

    # def get_queryset(self):
    #     queryset = self.request.user.client\
    #     .select_related('name')
    #     return queryset

@method_decorator([login_required,mechanic_required], name='dispatch')
class ClientDeleteView(DeleteView):
    model = ClientRepairs
    context_object_name = 'client'
    template_name = 'accounts/mechanic/client_repair_delete_form.html'
    success_url = reverse_lazy('mechanic:client_delete')

    def delete(self, request, *args, **kwargs):
        profile = self.get_object()
        messages.success(request, 'The client was deleted with success!')
        return super().delete(request, *args, **kwargs)





    # def get_queryset(self):
    #     return self.request.user.client

@method_decorator([login_required,mechanic_required], name='dispatch')
class ClientCreateView(CreateView):
    model = ClientRepairs
    context_object_name = 'client'
    fields = ('name','location','car_model','license_plate','phone_number','Issue')
    template_name = 'accounts/mechanic/client_add_form.html'


    def form_valid(self, form):
        mechprofile=form.save(commit=False)
        mechprofile.owner=self.request.user
        mechprofile.save()
        messages.success(self.request,'Profile Created with success')
        return redirect('mechanic:client_create')




class ClientUpdateView(UpdateView):
    model = ClientRepairs
    context_object_name = 'client'
    fields = ('name','location','car_model','license_plate','phone_number','Issue')
    template_name = 'accounts/mechanic/client_update_form.html'


    def form_valid(self, form):
        client=form.save(commit=False)
        client.owner=self.request.user
        client.save()
        messages.success(self.request,'ClientRepair with success')
        return redirect('mechanic:client_update')

    def get_success_url(self):
        return reverse('mechanic:client_update',kwargs={'pk':self.object.pk})


# @method_decorator([login_required,customer_required], name='dispatch')
# class MechanicDetailView(DetailView):
#     model = MechProfile
#     context_object_name = 'mechprofile'
#     template_name = 'accounts/mechanic/profile_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(MechanicDetailView, self).get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context


def profile_detail(request,mechprofile_id):
    mechprofile=get_object_or_404(MechProfile,pk=mechprofile_id)
    form=ReviewForm()
    return  render(request,'accounts/mechanic/profile_detail.html',{'mechprofile':mechprofile, 'form':form})

def add_review(request, mechprofile_id):
    mechprofile = get_object_or_404(MechProfile, pk=mechprofile_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.mechprofile = mechprofile
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mechanic:profile_detail', args=(mechprofile.id,)))

    return render(request, 'accounts/mechanic/profile_detail.html', {'mechprofile': mechprofile, 'form': form})
