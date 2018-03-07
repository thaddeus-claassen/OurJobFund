from django.conf.urls import include, url;
from django.contrib import admin;
from django.conf import settings;
from django.views.generic import TemplateView;
from django.conf.urls.static import static;
from django.contrib.auth import views as auth_views;
from user.views import SearchUsersView, see_more_users;
from job.views import home;
from update.views import CreateUpdateView, PayView;
from jobuser.views import WorkView, PledgeView;
from . import views;

app_name = 'ourjobfund';

urlpatterns = [
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'search-users$', SearchUsersView.as_view()),
    url(r'^see-more-users$', see_more_users),
    url(r'^admin/uwsgi/', include('django_uwsgi.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^job/', include('job.urls')),
    url(r'^$', home, name='home'),
    url(r'^update/', include('update.urls')),
    url(r'^update/create/(?P<job_random_string>[a-zA-Z0-9]+)/', CreateUpdateView.as_view(), name='create-update'),
    url(r'^pledge/(?P<job_random_string>[a-zA-Z0-9]+)', PledgeView.as_view(), name='pledge'),
    url(r'^work/(?P<job_random_string>[a-zA-Z0-9]+)', WorkView.as_view(), name='work'),
    url(r'^pay/(?P<username>[a-zA-Z0-9_]*)/(?P<job_random_string>[a-zA-Z0-9]+)/', PayView.as_view(), name='pay'),
    url(r'^about/', include('about.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^terms_of_service/', include('terms_of_service.urls')),
    url(r'^', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);

