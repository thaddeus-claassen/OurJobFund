from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'job';

urlpatterns = [

    # /job/
    url(r'^$', views.home, name='home'),

    # /job/add_job
    url(r'^add_job$', views.add_job, name='add_job'),
    
    # /job/add_location
    url(r'^add_location$', views.add_location, name='add_location'),
    
    # /job/search_jobs
    url(r'^search_jobs$', views.search_jobs, name='search_jobs'),
    
    # /job/apply_tags_and_location
    url(r'^apply_tags_and_location$', views.apply_tags_and_location, name="apply_tags_and_location"),
    
    # /job/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),
    
    # /job/<Job ID>/view_workers
    url(r'^(?P<job_id>[0-9]+)/view_workers$', views.view_workers, name='view_workers'),
    
    # /job/<Job ID>/become_main_editor
    url(r'^(?P<job_id>[0-9]+)/become_main_editor$', views.become_main_editor, name='become_main_editor'),     
    
    # /job/<Job ID>/pledge_money_to_job
    url(r'^(?P<job_id>[0-9]+)/pledge_money_to_job$', views.pledge_money_to_job, name='pledge_money_to_job'), 
    
    # /job/<Job ID>/work_on_job
    url(r'^(?P<job_id>[0-9]+)/work_on_job$', views.work_on_job, name='work_on_job'), 
    
    # /job/<Job ID>/description
    url(r'^(?P<job_id>[0-9]+)/description$', views.description, name='description'),
    
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);