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
    
    # /user/send_message
    url(r'^send_message$', views.send_message, name='send_message'),
    
    # /user/messages
    url(r'^messages$', views.messages, name='messages'),
    
    # /user/message/<message_id>
    url(r'^message/(?P<message_id>[0-9]+)$', views.message, name='message'),
    
    # /user/post_update/<workjob_id>
    url(r'^post_update/(?P<workjob_id>[0-9]+)$', views.post_update, name='post_update'), 
    
    # /user/update/<update_id>
    url(r'^update/(?P<update_id>[0-9]+)$', views.view_update, name='view_update'),

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
    
    # /user/detail/<user_username>
    url(r'^detail/(?P<user_username>[a-zA-Z0-9]+)$', views.detail, name='detail'),
]

if settings.DEBUG: # I don't understand what this does. I think something to do with needing to tell Django where the static files are when in testing mode, but I don't understand why it doesn't know where the static files are when the website is up and running
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);