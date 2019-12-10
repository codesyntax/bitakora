from django.conf.urls import url, include
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bitakora.views import DataGetCategories
from bitakora.base.models import Article
from voting.views import vote_on_object
from django.contrib.flatpages import views as flatpage_views
from bitakora import views
from bitakora.accounts import views as accounts_views
from bitakora.ikasbloga import views as ikasbloga_views
from django.contrib.auth import views as auth_views
from bitakora.accounts.views import BlogRegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

article_dict = {
    'model': Article,
    'template_object_name': 'article',
}


urlpatterns = [
    url(r'^$', views.index),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^category/(?P<slug>[\-\d\w]+)$', views.category, name='category'),
    url(r'^top_stories$', views.top_stories, name='top_stories'),
    url(r'^bookmarks$', views.bookmarks, name='bookmarks'),
    # url(r'^users$', auth_views.login, name='erabiltzailea_user_login'),
    # url(r'^users/password/change/$', accounts_views.edit_pass, name='pasahitza_aldatu'),
    # url(r'^users/password/change/done/$', accounts_views.pass_done, name='pasahitza_aldatuta'),
    url(r'^users/', include('registration.backends.default.urls')),
    url(r'^register/$', BlogRegistrationView.as_view(), name='registration_register'),
    url(r'^users/register/student$', accounts_views.student_registration, name='student_registration'),
    url(r'^users/register/teacher$', accounts_views.teacher_registration, name='teacher_registration'),
    url(r'^users/select-register$', accounts_views.select_register, name='select_register'),
    url(r'^users/useroptions$', views.useroptions, name='useroptions'),
    url(r'^users/edit-profile$', accounts_views.edit_profile, name='edit_profile'),
    url(r'^users/edit-blog$', accounts_views.edit_blog, name='edit_blog'),
    url(r'^users/edit-school$', ikasbloga_views.edit_school, name='edit_school'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/users/edit-profile', permanent=False), name='users_profile'),
    url(r'^ikasblogak', include('bitakora.ikasbloga.urls')),
    url(r'^voting/(?P<object_id>\d+)/(?P<direction>up|down|clear)?$', vote_on_object, article_dict, name="vote_on_object"),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),

    url(r'^ajax/get_categories$', DataGetCategories.as_view(), name='get_categories'),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^search/', include('haystack.urls')),

    url(r'^about$', flatpage_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^contact/', include('contact_form.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^ajax/categories/', views.get_categories, name='ajax_categories'),
    url(r'^ajax/related_posts/', views.get_related_posts, name='ajax_related_posts'),
    url(r'^ajax/remove_link/', views.remove_link, name='ajax_remove_link'),

    url(r'^', include('bitakora.base.urls')),
]

urlpatterns += staticfiles_urlpatterns()
