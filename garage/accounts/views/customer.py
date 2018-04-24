from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from ..suggestions import update_clusters
from ..decorators import customer_required
from ..forms import CustomerSignUpForm,ReviewForm
from ..models import User, Vehicle, CarHistory, Cluster, MechProfile, Review

import datetime

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
@login_required
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
        return HttpResponseRedirect(reverse('customer:mech_detail', args=(mechprofile.id,)))

    return render(request, 'customer/mechdetail', {'wine': mechprofile, 'form': form})

# @method_decorator([login_required,customer_required], name='dispatch')
# class ReviewCreateView(CreateView):
#     model = Review
#     context_object_name = 'review'
#     fields = 'mechprofile','rating','comment','user_name'
#     template_name = 'accounts/customer/review_add_form.html'
#
#     def form_valid(self, form):
#         review=form.save(commit=False)
#         review.owner=self.request.user
#         review.save()
#         update_clusters()
#         messages.success(self.request,"Review add successfully")
#         return redirect('customer:custdashboard')

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


def mech_list(request):
    mech_list = MechProfile.objects.order_by('-name')
    context = {'mech_list':mech_list}
    return render(request, 'accounts/customer/mech_list.html', context)

#initially a user can request for a mechanic even before they have used the site before
#essentially we eant to return mechanics not reviewed by the user
@login_required
def user_recommendation_list(request):
    #get user reviewed wines
    #we get a list of wine ids requested by the user
    user_reviews=Review.objects.filter(user_name=request.user.username).prefetch_related('mechprofile')
    user_reviews_mechprofile_ids=set(map(lambda x: x.mechprofile.id, user_reviews))


    # get request user cluster name (just the first one right now)
    # so here just want to get the cluster name the request user belongs to
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    #get usernames for other members of the cluster
    #exlude the request user just to reduce query time
    user_cluster_other_members =\
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users(in the cluster),excluding wines reviewed by the request user
    other_users_reviews =\
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(mechprofile__id__in=user_reviews_mechprofile_ids)
    other_users_reviews_mechprofile_ids= set(map(lambda x: x.mechprofile.id, other_users_reviews))

    #then get a mechanic list including the previous IDS,order by rating

    mech_list=sorted(
        list(MechProfile.objects.filter(id__in=other_users_reviews_mechprofile_ids)),
        key=lambda  x: x.average_rating(),
        reverse=True
    )


    return render(
        request,
        'accounts/customer/user_recommendation_list.html',
        {'username': request.user.username,'mech_list': mech_list}
    )
