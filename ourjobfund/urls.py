from django.conf.urls import include, url;
from django.contrib import admin;
from django.conf import settings;
from django.views.generic import TemplateView;
from django.conf.urls.static import static;
from django.contrib.auth import views as auth_views;
from user.views import SearchUsersView, see_more_users;
from job.views import home;
from update.views import CreateUpdateView;
from pay.views import PayView;
from jobuser.views import WorkView, PledgeView;
from .acceptable_urls import URLS;

app_name = 'ourjobfund';

urlpatterns = [
    url(r'^' + URLS['robots'] + '/$', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),
    url(r'^' + URLS['password_reset'] + '/$', auth_views.password_reset, name='password_reset'),
    url(r'^' + URLS['password_reset'] + '/' + URLS['done'] + '/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^' + URLS['reset'] + '/' + URLS['uidb66_regex'] + '/' + URLS['token_regex'] + '/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^' + URLS['reset'] + '/' + URLS['done'] + '/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'' + URLS['search-users'] + '/$', SearchUsersView.as_view()),
    url(r'^' + URLS['see-more-users'] + '/$', see_more_users),
    url(r'^' + URLS['admin'] + '/', admin.site.urls),
    url(r'^' + URLS['job'] + '/', include('job.urls')),
    url(r'^$', home, name='home'),
    url(r'^' + URLS['update'] + '/', include('update.urls')),
    url(r'^' + URLS['update'] + '/' + URLS['create'] + '/' + URLS['job_random_string_regex'] + '/', CreateUpdateView.as_view(), name='create-update'),
    url(r'^' + URLS['pledge'] + '/' + URLS['job_random_string_regex'] + '/$', PledgeView.as_view(), name='pledge'),
    url(r'^' + URLS['work'] + '/' + URLS['job_random_string_regex'] + '/$', WorkView.as_view(), name='work'),
    url(r'^' + URLS['pay'] + '/' + URLS['username_regex'] + '/$', PayView.as_view(), name='pay'),
    url(r'^' + URLS['about'] + '/', include('about.urls')),
    url(r'^' + URLS['contact'] + '/', include('contact.urls')),
    url(r'^' + URLS['terms_of_service'] + '/', include('terms_of_service.urls')),
    url(r'^', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT);
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);

