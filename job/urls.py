from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'job';

urlpatterns = [

    # /job/
    url(r'^$', views.home, name='home'),
    
    # /job/create_job
    url(r'^create_job/$', views.create_job, name='create_job'),
    
    # /job/get_jobs
    url(r'^get_jobs/$', views.get_jobs),
    
    # /job/add_jobs
    url(r'^add_jobs/$', views.add_jobs),
    
    # /job/sort_jobs
    url(r'^sort_jobs/$', views.sort_jobs),
    
    # /job/get_total_jobs
    url(r'^get_total_jobs/$', views.get_total_jobs),

    # /job/<Job Random String>
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/$', views.detail, name='detail'),
    
    #/job/<Job Random String>/sort
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/sort/$', views.detail_sort),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);