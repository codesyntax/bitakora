from django.conf.urls import url
from bitakora.ikasbloga import views
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^(?P<slug>[\-\d\w]+)$', views.dashboard, name='school_dashboard'),
    url(r'^$', views.index, name='school_blogs'),    
]
