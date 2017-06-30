from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jobuser';

urlpatterns = [

    # /jobuser/post_update/<jobuser_id>
    url(r'^post_update/(?P<jobuser_id>[0-9]+)/$', views.post_update, name='post_update'), 
    
    # /jobuser/update/<update_id>
    url(r'^update/(?P<update_id>[0-9]+)/$', views.view_update, name='view_update'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);