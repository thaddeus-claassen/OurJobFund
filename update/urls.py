from django.conf.urls import url;
from . import views;
from django.conf import settings;
from django.conf.urls.static import static;
from ourjobfund.acceptable_urls import URLS;

app_name = 'update';

urlpatterns = [
    url(r'^' + URLS['create'] + '/' + URLS['job_random_string_regex'] + '/$', views.CreateUpdateView.as_view(), name='create'),
    url(r'^' + URLS['update_random_string_regex'] + '/' + URLS['images'] + '/$', views.images, name='images'),
    url(r'^' + URLS['delete'] + '/' + URLS['update_random_string_regex'] + '/$', views.DeleteUpdateView.as_view(), name='delete'),
];