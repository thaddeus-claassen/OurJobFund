from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'terms_of_service';

urlpatterns = [

    # /terms-of-service/
    url(r'^$', views.termsOfService, name='terms_of_service'),

]