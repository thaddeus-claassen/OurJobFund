from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'job';

urlpatterns = [

    # /job/
    url(r'^$', views.home, name='home'),
    
    # /job/see_more_jobs
    url(r'^see_more_jobs/$', views.see_more_jobs, name='see_more_jobs'),

    # /job/add_job
    url(r'^add_job/$', views.add_job, name='add_job'),
    
    # /job/apply_tags_and_location
    url(r'^apply_tags_and_location/$', views.apply_tags_and_location, name="apply_tags_and_location"),
    
    # /job/<Job Random String>
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/$', views.detail, name='detail'),   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);