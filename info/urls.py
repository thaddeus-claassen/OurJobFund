from django.conf.urls import url;
from django.conf import settings;
from . import views;
from django.conf.urls.static import static;

app_name = 'info';

urlpatterns = [
        
    url(r'^about/$', views.about, name='about'),
    
    url(r'^contact/$', views.contact, name='contact'),
    
    url(r'^terms-of-agreement/$', views.termsOfAgreement, name='terms-of-agreement'),
    
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);
