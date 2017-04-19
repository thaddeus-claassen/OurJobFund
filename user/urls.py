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
    
    # /user/search_users
    url(r'^search_users$', views.search_users, name='search_users'),
    
    # /user/messages/send_message
    url(r'^messages/send_message$', views.send_message),
    
    # /user/detail/send_message
    url(r'^detail/send_message$', views.send_message, name='send_message'),
    
    # /user/view_messages_by_user
    url(r'^view_messages_by_user$', views.view_messages_by_user, name='view_messages_by_user'),
    
    # /user/messages/other_user_username
    url(r'^messages/(?P<user_username>[a-zA-Z0-9]+)$', views.messages, name='messages'),
    
    # /user/messages/get_messages
    url(r'^messages/get_messages$', views.get_messages, name='get_messages'),

    # /user/detail/save_description/
    url(r'^detail/save_description$', views.save_description, name='save_description'),
    
    # /user/change_public_pledge_filter
    url(r'^change_public_pledge_filter$', views.change_public_pledge_filter, name='change_public_pledge_filter'),
    
    # /user/change_public_worker_filter
    url(r'^change_public_worker_filter$', views.change_public_worker_filter, name='change_public_worker_filter'),
    
    # /user/copy_pledge_filter
    url(r'^copy_pledge_filter$', views.copy_pledge_filter),
    
    # /user/copy_worker_filter
    url(r'^copy_worker_filter$', views.copy_worker_filter),
    
    # /user/<user_username>
    url(r'^detail/(?P<user_username>[a-zA-Z0-9]+)$', views.detail, name='detail'),
    
    # /user/get_user_info
    url(r'^detail/get_user_info$', views.get_user_info),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);