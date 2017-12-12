from django.conf import settings;
from django.conf.urls import url;
from django.conf.urls.static import static;
from . import views;

app_name = 'job';

urlpatterns = [
    url(r'^$', views.redirect_to_home),
    url(r'^home$', views.home, name='home'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^save_filter/$', views.save_filter),
    url(r'^save_search_type/$', views.save_search_type),
    url(r'^save_hide_location/$', views.save_hide_location),
    url(r'^get_jobs/$', views.get_jobs),
    url(r'^add_jobs/$', views.add_jobs),
    url(r'^sort_jobs/$', views.sort_jobs),
    url(r'^get_total_jobs/$', views.get_total_jobs),
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<job_random_string>[a-zA-Z0-9]+)/sort/$', views.detail_sort),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);