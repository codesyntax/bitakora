from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bitakora.views import DataGetCategories
from bitakora.base.models import Article
from voting.views import vote_on_object
from django.contrib.flatpages import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

article_dict = {
    'model': Article,
    'template_object_name': 'article',
}


urlpatterns = patterns('',
    (r'^$','bitakora.views.index'),
    (r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^category/(?P<slug>[\-\d\w]+)$','bitakora.views.category', name='category'),
    url(r'^top_stories$', 'bitakora.views.top_stories', name='top_stories'),
    url(r'^bookmarks$', 'bitakora.views.bookmarks', name='bookmarks'),
    url(r'^users$','django.contrib.auth.views.login', name='erabiltzailea_user_login'),
    url(r'^users/useroptions$','bitakora.views.useroptions', name='useroptions'),
    url(r'^users/edit-profile$','bitakora.accounts.views.edit_profile', name='edit_profile'),
    url(r'^users/edit-blog$','bitakora.accounts.views.edit_blog', name='edit_blog'),
    url(r'^users/accounts/password/change/$','bitakora.accounts.views.edit_pass', name='pasahitza_aldatu'),
    url(r'^users/accounts/password/change/done/$','bitakora.accounts.views.pass_done', name='pasahitza_aldatuta'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/users/edit-profile', permanent=False), name='users_profile'),
    (r'^users/accounts', include('registration.backends.default.urls')),
    (r'^users/', include('cssocialuser.urls')),

    url(r'^voting/(?P<object_id>\d+)/(?P<direction>up|down|clear)?$', vote_on_object, article_dict, name="vote_on_object"),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),

    url(r'^ajax/get_categories$', DataGetCategories.as_view(), name='get_categories'),

    (r'^tinymce/', include('tinymce.urls')),

    (r'^search/', include('haystack.urls')),

    url(r'^about$', views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^contact/', include('contact_form.urls')),

    (r'^admin/', include(admin.site.urls)),

    url(r'^ajax/categories/', 'bitakora.views.get_categories', name='ajax_categories'),
    url(r'^ajax/related_posts/', 'bitakora.views.get_related_posts', name='ajax_related_posts'),
    url(r'^ajax/remove_link/', 'bitakora.views.remove_link', name='ajax_remove_link'),

    (r'^', include('bitakora.base.urls')),
)

urlpatterns += staticfiles_urlpatterns()