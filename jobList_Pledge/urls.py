from django.conf.urls import url
from . import views

urlpatterns = [
    # /jobList_Pledge/
    url(r'^$', views.index, name='index'),

    # /jobList_Pledge/<Job ID>
    url(r'^(?P<job_id>[0-9]+)$', views.detail, name='detail'),
]