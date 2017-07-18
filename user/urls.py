from django.conf.urls import url;
from . import views;
from django.conf import settings;
from django.conf.urls.static import static;

app_name = 'user';

urlpatterns = [

    # /user/sign_in
    url(r'^sign_in/$', views.sign_in, name="sign_in"),
    
    # /user/sign_out
    url(r'^sign_out/&', views.sign_out, name="sign_out"),
    
    # /user/<username>
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.detail, name='detail'),
    
    # /user/search_users
    url(r'^search_users/$', views.search_users, name='search_users'),
    
    # /user/see_more_users
    url(r'^see_more_users/$', views.see_more_users, name='see_more_users'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);