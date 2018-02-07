from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'update';

urlpatterns = [
    url(r'^(?P<update_random_string>[a-zA-Z0-9]+)/$', views.detail, name='detail'),
    url(r'^create/(?P<job_random_string>[a-zA-Z0-9]+)/$', views.CreateView.as_view(), name='create'), 
]