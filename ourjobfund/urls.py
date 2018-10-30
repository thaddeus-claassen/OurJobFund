from django.conf.urls import include, url;
from django.urls import path;
from django.contrib import admin;
from django.conf import settings;
from django.views.generic import TemplateView;
from django.conf.urls.static import static;
from django.contrib.auth import views as auth_views;
from user.views import search_user;
from job.views import home;
from jobuser.views import PledgeView, WorkView, FinishView, PledgeHistoryView, WorkHistoryView, sort_pledge_history, sort_work_history;
from jobuser.views import StripePayTestView;
from .acceptable_urls import URLS;

app_name = 'ourjobfund';

urlpatterns = [
    url(r'^pay/$', StripePayTestView.as_view()),
    url(r'^' + URLS['robots'] + '/$', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),
    path('' + URLS['accounts'] + '/', include('django.contrib.auth.urls')),
    url(r'' + URLS['search-user'] + '/$', search_user),
    url(r'^' + URLS['admin'] + '/', admin.site.urls),
    url(r'^' + URLS['job'] + '/', include('job.urls')),
    url(r'^$', home, name='home'),
    url(r'^' + URLS['update'] + '/', include('update.urls')),
    url(r'^' + URLS['pledge'] + '/' + URLS['job_random_string_regex'] + '/$', PledgeView.as_view(), name='pledge'),
    url(r'^' + URLS['pledge-history'] + '/' + URLS['job_random_string_regex'] + '/$', PledgeHistoryView.as_view(), name='pledge-history'),
    url(r'^' + URLS['pledge-history'] + '/' + URLS['job_random_string_regex'] + '/' + URLS['sort'] + '/$', sort_pledge_history),
    url(r'^' + URLS['work'] + '/' + URLS['job_random_string_regex'] + '/$', WorkView.as_view(), name='work'),
    url(r'^' + URLS['work-history'] + '/' + URLS['job_random_string_regex'] + '/$', WorkHistoryView.as_view(), name='work-history'),
    url(r'^' + URLS['work-history'] + '/' + URLS['job_random_string_regex'] + '/' + URLS['sort'] + '/$', sort_work_history),
    url(r'^' + URLS['finish'] + '/' + URLS['job_random_string_regex'] + '/$', FinishView.as_view(), name='finish'),
    url(r'^' + URLS['about'] + '/', include('about.urls')),
    url(r'^' + URLS['contact'] + '/', include('contact.urls')),
    url(r'^' + URLS['terms_of_service'] + '/', include('terms_of_service.urls')),
    url(r'^' + URLS['privacy'] + '/', include('privacy.urls')),
    url(r'^' + URLS['user'] + '/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);

