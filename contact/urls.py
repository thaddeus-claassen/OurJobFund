from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'contact';

urlpatterns = [

    # /contact/
    url(r'^$', views.contact, name='contact'),

]