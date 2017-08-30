from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'update';

urlpatterns = [
    # /update/create/
    url(r'^create/(?P<job_random_string>[a-zA-Z0-9]+)/$', views.create, name='create'), 
    
    # /update/job_random_string>
    url(r'^(?P<update_random_string>[0-9]+)/$', views.detail, name='detail'),
]