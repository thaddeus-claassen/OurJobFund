from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pledge';

urlpatterns = [
    url(r'^index$', views.index_pledge, name='home'),
    
    # /pledge/login_pledge
    url(r'^login_pledge$', views.login_pledge, name="login_pledge"),
    
    # /pledge/logout_pledge
    url(r'^logout_pledge$', views.logout_pledge, name='logout_pledge'),
    
    # /pledge/
    url(r'^$', views.index_pledge, name='index'),

    # /pledge/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),

    # /pledge/<Job ID>/user_is_working_on_job
    url(r'^(?P<job_id>[0-9]+)/user_is_working_on_job$', views.user_is_working_on_job, name='user_is_working_on_job'), 
    
    # /pledge/<Job ID>/work_on_job
    url(r'^(?P<job_id>[0-9]+)/work_on_job$', views.work_on_job, name='work_on_job'), 

    # /pledge/add_job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /pledge/add_location
    url(r'^add_location$', views.add_location, name='add_location'),
    
    # /pledge/create_job
    url(r'^create_job$', views.create_job, name='create_job'),
    
    # /pledge/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /pledge/apply_tags_and_location
    url(r'^apply_tags_and_location$', views.apply_tags_and_location, name="apply_tags_and_location"),
    
    # /pledge/ANDs_of_ORs
    url(r'^ANDs_of_ORs$', views.ANDs_of_ORs, name='ANDs_of_ORs'),
    
    # /pledge/save_ANDs_of_ORs_tags
    url(r'^save_ANDs_of_ORs_tags$', views.save_ANDs_of_ORs_tags, name='save_ANDs_of_ORs_tags'),
    
    # /pledge/get_ANDs_of_ORs_tags
    url(r'^get_ANDs_of_ORs_tags$', views.get_ANDs_of_ORs_tags, name='get_ANDs_of_ORs_tags'),
    
    # /pledge/ORs_of_ANDs
    url(r'^ORs_of_ANDs$', views.ORs_of_ANDs, name='ORs_of_ANDs'),
    
    # /pledge/save_ORs_of_ANDs_tags
    url(r'^save_ORs_of_ANDs_tags$', views.save_ORs_of_ANDs_tags, name='save_ORs_of_ANDs_tags'),
    
    # /pledge/get_ORs_of_ANDs_tags
    url(r'^get_ORs_of_ANDs_tags$', views.get_ORs_of_ANDs_tags, name='get_ORs_of_ANDs_tags'),
    
    # /pledge/custom
    url(r'^custom$', views.custom, name='custom'),
    
    # /pledge/save_custom_tags
    url(r'^save_custom_tags$', views.save_custom_tags, name='save_custom_tags'),
    
    # /pledge/get_custom_tags
    url(r'^get_custom_tags$', views.get_custom_tags, name='get_custom_tags'),
    
    # /pledge/view_all_metrics_pledge
    url(r'^view_all_metrics_pledge$', views.view_all_metrics_pledge, name='view_all_metrics_pledge'),
    
    # /pledge/apply_metrics_pledge
    url(r'^apply_metrics_pledge$', views.apply_metrics_pledge, name='apply_metrics_pledge'), 
    
    # /pledge/clear_metrics_pledge
    url(r'^clear_metrics$', views.clear_metrics, name='clear_metrics'),
    
    # /pledge/apply_metrics
    url(r'^apply_metrics$', views.apply_metrics, name='apply_metrics'),
    
    # /pledge/<Job ID>/description
    url(r'^(?P<job_id>[0-9]+)/description$', views.description, name='description'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);