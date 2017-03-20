from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jobuser';

urlpatterns = [

    # /jobuser/post_update/<workjob_id>
    url(r'^post_update/(?P<workjob_id>[0-9]+)$', views.post_update, name='post_update'), 
    
    # /jobuser/update/<update_id>
    url(r'^update/(?P<update_id>[0-9]+)$', views.view_update, name='view_update'),
    
    # /jobuser/update/publish_comment
    url(r'^update/publish_comment$', views.publish_comment),
    
    # /jobuser/comment/publish_comment
    url(r'^comment/publish_comment$', views.publish_comment),
    
    # /jobuser/comment/<comment_id>
    url(r'^comment/(?P<comment_id>[0-9]+)$', views.view_comment, name='view_comment'),
    
    # /jobuser/view_updates/<workjob_id>
    url(r'^view_updates/(?P<workjob_id>[0-9]+)$', views.view_updates, name='view_updates'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);