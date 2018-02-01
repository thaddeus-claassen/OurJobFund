from django.conf.urls import url;
from . import views;
from django.conf import settings;
from django.conf.urls.static import static;

app_name = 'user';

urlpatterns = [
    url(r'^log-in/$', views.LoginView.as_view(), name='login'),
    url(r'^sign-out/&', views.sign_out, name='sign_out'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^search-users/$', views.SearchUsersView.as_view(), name='search_users'),
    url(r'^see-more-users/$', views.see_more_users, name='see_more_users'),
    url(r'^(?P<username>[a-zA-Z0-9_]*)/$', views.DetailView.as_view(), name='detail'),
]
