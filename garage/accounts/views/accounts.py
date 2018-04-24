from django.contrib.auth import login
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.shortcuts import redirect,render,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..models import User,Vehicle,CarHistory,Review,Cluster

from ..forms import CustomerSignUpForm
from ..decorators import customer_required
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Avg, Count
from django.views.generic import View
from django.template.loader import get_template
from ..utils import render_to_pdf #created in step 4


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

# from weasyprint import HTML
#
# def html_to_pdf_view(request):
#     paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#     html_string = render_to_string('core/pdf_template.html', {'paragraphs': paragraphs})
#
#     html = HTML(string=html_string)
#     html.write_pdf(target='/tmp/mypdf.pdf');
#
#     fs = FileSystemStorage('/tmp')
#     with fs.open('mypdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#         return response
#     return response
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_mechanic:
            return redirect('mechanic:mechdashboard')
        else:
            return redirect('customer:custdashboard')
    return render(request, 'accounts/home.html')

# @method_decorator([login_required,customer_required], name='dispatch')
# class RateCreateView(CreateView):
#     model = Review
#     context_object_name = 'review'
#     fields = ('mechanicname','rating','customer_name','comment','pub_date')
#     template_name = 'accounts/ratings/rate_add_form.html'
#
#
#     def form_valid(self, form):
#         review=form.save(commit=False)
#         user_name = request.user.username
#         review = Review()
#         review.wine = wine
#         review.user_name = user_name
#         review.rating = rating
#         review.comment = comment
#         review.pub_date = datetime.datetime.now()
#         review.save()
#         update_clusters()
#         return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
# @login_required
# def add_review(request, wine_id):
#     wine = get_object_or_404(Wine, pk=wine_id)
#     form = ReviewForm(request.POST)
#     if form.is_valid():
#         rating = form.cleaned_data['rating']
#         comment = form.cleaned_data['comment']
#         user_name = request.user.username
#         review = Review()
#         review.wine = wine
#         review.user_name = user_name
#         review.rating = rating
#         review.comment = comment
#         review.pub_date = datetime.datetime.now()
#         review.save()
#         update_clusters()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
#    9
#
#
# @method_decorator([login_required,customer_required], name='dispatch')
# class RateListView(ListView):
#      model = Review
#      context_object_name = 'review'
#      template_name = 'accounts/ratings/rate_list.html'
#
#
#      def get_queryset(self):
#         queryset=self.request.user.review\
#             .select_related('customer_name')
#         return queryset
#
# @login_required
# def user_recommendation_list(request):
#
#     # get request user reviewed wines
#     user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
#     user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))
#
#     # get request user cluster name (just the first one righ now)
#     user_cluster_name = \
#         User.objects.get(username=request.user.username).cluster_set.first().name
#
#     # get usernames for other members of the cluster
#     user_cluster_other_members = \
#         Cluster.objects.get(name=user_cluster_name).users \
#             .exclude(username=request.user.username).all()
#     other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))
#
#     # get reviews by those users, excluding wines reviewed by the request user
#     other_users_reviews = \
#         Review.objects.filter(user_name__in=other_members_usernames) \
#             .exclude(wine__id__in=user_reviews_wine_ids)
#     other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))
#
#     # then get a wine list including the previous IDs, order by rating
#     wine_list = sorted(
#         list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)),
#         key=lambda x: x.average_rating,
#         reverse=True
#     )
#
#     return render(
#         request,
#         'ratings/user_recommendation_list.html',
#         {'username': request.user.username,'wine_list': wine_list}
#     )
