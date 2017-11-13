from django.conf.urls import url;
from . import views;
from django.conf import settings;
from django.conf.urls.static import static;

app_name = 'user';

urlpatterns = [
    url(r'^$', views.SignUpView.as_view()),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^sign_up/$', views.SignUpView.as_view(), name='sign_up'),
    url(r'^sign_out/&', views.sign_out, name='sign_out'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^(?P<username>[a-zA-Z0-9]*)/$', views.DetailView.as_view(), name='detail'),
    url(r'^search_users/$', views.search_users, name='search_users'),
    url(r'^see_more_users/$', views.see_more_users, name='see_more_users'),
]
