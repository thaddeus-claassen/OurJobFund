from django.conf.urls import url;
from . import views;
from django.conf import settings;
from ourjobfund.acceptable_urls import URLS;
from django.conf.urls.static import static;

app_name = 'user';

urlpatterns = [
    url(r'^' + URLS['stripe'] + '/$', views.stripe, name='stripe'),
    url(r'^' + URLS['log-in'] + '/$', views.LoginView.as_view(), name='login'),
    url(r'^' + URLS['sign-out'] + '/$', views.sign_out, name='sign_out'),
    url(r'^' + URLS['account'] + '/$', views.AccountView.as_view(), name='account'),
    url(r'^' + URLS['username_regex'] + '/$', views.DetailView.as_view(), name='detail'),
    url(r'^' + URLS['username_regex'] + '/' + URLS['sort'] + '/$', views.add_to_detail_table),
]
