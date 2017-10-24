from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'job';

urlpatterns = [
    url(r'^$', views.get_stripe_info),
    url(r'^pledge$', views.pledge, name='pledge'),
    url(r'^work$', views.work, name='work'),
    url(r'^create_job/$', views.create_job, name='create_job'),
    url(r'^get_jobs/$', views.get_jobs),
    url(r'^add_jobs/$', views.add_jobs),
    url(r'^sort_jobs/$', views.sort_jobs),
    url(r'^get_total_jobs/$', views.get_total_jobs),
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/sort/$', views.detail_sort),
    url(r'^confirmation/(?P<job_random_string>[a-zA-Z0-9]+)', views.payment_confirmation, name='confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);