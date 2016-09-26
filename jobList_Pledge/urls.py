from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /jobList_Pledge/
    url(r'^$', views.index, name='index'),

    # /jobList_Pledge/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),

    # /jobList_Pledge/Add_Job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /jobList_Pledge/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /jobList_Pledge/apply_basic_hashtags
    url(r'^apply_basic_hashtags$', views.apply_basic_hashtags, name='apply_basic_hashtags'),
    
    # /jobList_Pledge/ANDs_of_ORs
    url(r'^ANDs_of_ORs$', views.ANDs_of_ORs, name='ANDs_of_ORs'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);