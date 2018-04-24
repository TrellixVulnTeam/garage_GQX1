from django.contrib.auth import login
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.shortcuts import redirect,render,reverse
from django.contrib import  messages
from ..models import User,MechProfile
from ..forms import MechanicSignUpForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import mechanic_required
from django.urls import reverse_lazy
def mechdashboard(request):
    items = Quiz.objects.all()
    return render(request,'accounts/mechanic/mechdashboard.html',context={'items':items})


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
    fields = ('garage_name','county','desc','profile_photo')
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
    fields = ('garage_name','county','desc','profile_photo')
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


@method_decorator([login_required,mechanic_required], name='dispatch')
class MechListView(ListView):
    model = MechProfile
    ordering = ('user_name', )
    context_object_name = 'mechprofile'
    template_name = 'accounts/mechanic/profile_list.html'

    def get_queryset(self):
        queryset = self.request.user.mechprofile\
        .select_related('owner')
        return queryset

