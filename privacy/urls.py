from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'privacy';

urlpatterns = [

    url(r'^$', views.privacy, name='privacy'),

]