from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /JobList/
    url(r'^$', views.index, name='index'),

    # /JobList/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),

    # /JobLsit/add_job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /JobList/create_job
    url(r'^create_job$', views.create_job, name='create_job'),
    
    # /JobList/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /JobList/search_jobs_by_radius
    url(r'^search_jobs_by_radius$', views.search_jobs_by_radius, name='search_jobs_by_radius'),
    
    # /JobList/apply_basic_hashtags
    url(r'^apply_basic_hashtags$', views.apply_basic_hashtags, name='apply_basic_tags'),
    
    # /JobList/ANDs_of_ORs
    url(r'^ANDs_of_ORs$', views.ANDs_of_ORs, name='ANDs_of_ORs'),
    
    # /JobList/custom_logic
    url(r'^custom_logic$', views.custom_logic, name='custom_logic'),
    
    # /JobList/view_all_metrics_pledge
    url(r'^view_all_metrics_pledge$', views.view_all_metrics_pledge, name='view_all_metrics_pledge'),
    
    # /JobList/apply_metrics
    url(r'^apply_metrics$', views.apply_metrics, name='apply_metrics'),
    
    # /JobList/<Job ID>/description
    url(r'^(?P<job_id>[0-9]+)/description$', views.description, name='description'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    