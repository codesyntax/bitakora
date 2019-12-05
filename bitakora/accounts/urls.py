from django.conf.urls import url, include
from django.contrib.auth import views as login_views
from tokikom import views

urlpatterns = [
    url(r'^$', login_views.login, name='erabiltzailea_user_login'),
    url(r'^useroptions$', views.useroptions, name='erabiltzailea_useroptions'),
    url(r'^change_pass/$', login_views.password_change, name='pasahitza_aldatu'),
    url(r'^accounts$', include('registration.backends.default.urls')),
    url(r'', include('cssocialuser.urls')),
]