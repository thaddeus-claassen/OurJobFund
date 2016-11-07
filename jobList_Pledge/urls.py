from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /jobList_Pledge/
    url(r'^$', views.index, name='index'),

    # /jobList_Pledge/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),

    # /jobList_Pledge/add_job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /jobList_Pledge/create_job
    url(r'^create_job$', views.create_job, name='create_job'),
    
    # /jobList_Pledge/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /jobList_Pledge/search_jobs_by_radius
    url(r'^search_jobs_by_radius$', views.search_jobs_by_radius, name='search_jobs_by_radius'),
    
    # /jobList_Pledge/apply_basic_hashtags
    url(r'^apply_basic_hashtags$', views.apply_basic_hashtags, name='apply_basic_tags'),
    
    # /jobList_Pledge/ANDs_of_ORs
    url(r'^ANDs_of_ORs$', views.ANDs_of_ORs, name='ANDs_of_ORs'),
    
    # /jobList_Pledge/view_all_metrics_pledge
    url(r'^view_all_metrics_pledge$', views.view_all_metrics_pledge, name='view_all_metrics_pledge'),
    
    # /jobList_Pledge/apply_metrics
    url(r'^apply_metrics$', views.apply_metrics, name='apply_metrics'),
    
    # /jobList_Pledge/<Job ID>/description
    url(r'^(?P<job_id>[0-9]+)/description$', views.description, name='description'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    