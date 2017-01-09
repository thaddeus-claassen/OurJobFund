from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index$', views.index, name='home'),
    
    # /JobList/
    url(r'^$', views.index, name='index'),

    # /JobList/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),

    # /JobList/add_job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /JobList/add_location
    url(r'^add_location$', views.add_location, name='add_location'),
    
    # /JobList/create_job
    url(r'^create_job$', views.create_job, name='create_job'),
    
    # /JobList/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /JobList/search_jobs_by_radius
    url(r'^search_jobs_by_radius$', views.search_jobs_by_radius, name='search_jobs_by_radius'),
    
    # /JobList/apply_tag_basic_logic_and_location
    url(r'^apply_tag_basic_logic_and_location$', views.apply_tag_basic_logic_and_location, name='apply_tag_basic_logic_and_location'),
    
    # /JobList/apply_tag_basic_logic
    url(r'^apply_tag_basic_logic$', views.apply_tag_basic_logic, name='apply_tag_basic_logic'),
    
    # /JobList/apply_tag_ANDs_of_ORs_logic
    url(r'^apply_tag_ANDs_of_ORs_logic$', views.apply_tag_ANDs_of_ORs_logic, name='apply_tag_ANDs_of_ORs_logic'),
    
    # /JobList/apply_tag_ORs_of_ANDs_logic
    url(r'^apply_tag_ORs_of_ANDs_logic$', views.apply_tag_ORs_of_ANDs_logic, name='apply_tag_ORs_of_ANDs_logic'),
    
    # /JobList/apply_tag_custom_logic
    url(r'^apply_tag_custom_logic$', views.apply_tag_custom_logic, name='apply_tag_custom_logic'),
    
    # /JobList/ANDs_of_ORs
    url(r'^ANDs_of_ORs$', views.ANDs_of_ORs, name='ANDs_of_ORs'),
    
    # /JobList/save_ANDs_of_ORs_tags
    url(r'^save_ANDs_of_ORs_tags$', views.save_ANDs_of_ORs_tags, name='save_ANDs_of_ORs_tags'),
    
    # /JobList/get_ANDs_of_ORs_tags
    url(r'^get_ANDs_of_ORs_tags$', views.get_ANDs_of_ORs_tags, name='get_ANDs_of_ORs_tags'),
    
    # /JobList/ORs_of_ANDs
    url(r'^ORs_of_ANDs$', views.ORs_of_ANDs, name='ORs_of_ANDs'),
    
    # /JobList/save_ORs_of_ANDs_tags
    url(r'^save_ORs_of_ANDs_tags$', views.save_ORs_of_ANDs_tags, name='save_ORs_of_ANDs_tags'),
    
    # /JobList/get_ORs_of_ANDs_tags
    url(r'^get_ORs_of_ANDs_tags$', views.get_ORs_of_ANDs_tags, name='get_ORs_of_ANDs_tags'),
    
    # /JobList/custom
    url(r'^custom$', views.custom, name='custom'),
    
    # /JobList/save_custom_tags
    url(r'^save_custom_tags$', views.save_custom_tags, name='save_custom_tags'),
    
    # /JobList/get_custom_tags
    url(r'^get_custom_tags$', views.get_custom_tags, name='get_custom_tags'),
    
    # /JobList/view_all_metrics_pledge
    url(r'^view_all_metrics_pledge$', views.view_all_metrics_pledge, name='view_all_metrics_pledge'),
    
    # /JobList/apply_metrics
    url(r'^apply_metrics$', views.apply_metrics, name='apply_metrics'),
    
    # /JobList/<Job ID>/description
    url(r'^(?P<job_id>[0-9]+)/description$', views.description, name='description'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);