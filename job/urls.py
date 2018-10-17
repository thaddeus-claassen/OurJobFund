from django.conf import settings;
from django.conf.urls import include, url;
from django.conf.urls.static import static;
from ourjobfund.acceptable_urls import URLS;
from . import views;
from jobuser.views import MiscPayView, StripePayView, ModerateView, BanUserView, ConfirmPayView;

app_name = 'job';

urlpatterns = [
    url(r'^' + URLS['create'] + '/$', views.CreateView.as_view(), name='create'),
    url(r'^' + URLS['get-jobs'] + '/$', views.get_jobs),
    url(r'^' + URLS['get-total-jobs'] + '/$', views.get_total_jobs),
    url(r'^' + URLS['job_random_string_regex'] + '/$', views.DetailView.as_view(), name='detail'),
    url(r'^' + URLS['job_random_string_regex'] + '/' + URLS['sort'] + '/$', views.add_to_detail_table),
    url(r'^' + URLS['job_random_string_regex'] + '/' + URLS['moderate'] + '/$', ModerateView.as_view(), name='moderate'),
    url(r'^' + URLS['ban-user'] + '/' + URLS['jobuser_random_string_regex'] + '/$', BanUserView.as_view(), name='ban-user'),
    url(r'^' + URLS['job_random_string_regex'] + '/' + URLS['username_regex'] + '/' + URLS['stripe-pay'] + '/$', StripePayView.as_view(), name='stripe-pay'),
    url(r'^' + URLS['job_random_string_regex'] + '/' + URLS['misc-pay'] + '/$', MiscPayView.as_view(), name='misc-pay'),
    url(r'^' + URLS['job_random_string_regex'] + '/' + URLS['confirm-pay'] + '/$', ConfirmPayView.as_view(), name='confirm-pay'),
];

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);