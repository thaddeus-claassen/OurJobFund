"""TheWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url;
from django.contrib import admin;
from django.conf import settings;
from django.conf.urls.static import static;
from user.views import get_messages_for_navbar, get_num_unviewed_messages;
from jobuser.views import view_pledge_notification, view_work_notification;
from . import views;

app_name = 'TheWebsite';

urlpatterns = [
    url(r'get_messages_for_navbar$', get_messages_for_navbar),
    url(r'get_num_unviewed_messages$', get_num_unviewed_messages),
    url(r'view_pledge_notification/(?P<notification_id>[0-9]+)$', view_pledge_notification),
    url(r'view_work_notification/(?P<notification_id>[0-9]+)$', view_work_notification),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls')),
    url(r'^job/', include('job.urls')),
    url(r'^jobuser/', include('jobuser.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', views.index, name='index'),
]

if (settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
