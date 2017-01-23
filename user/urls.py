from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user';

urlpatterns = [
 
    # /user/create_user
    url(r'^create_user$', views.create_user, name='create_user'),
    
    # /user/verify_username
    url(r'^verify_username$', views.verify_username, name='verify_username'),
    
    # /user/<User ID>
    url(r'^(?P<user_id>[0-9]+)$', views.detail, name='detail'),    
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);