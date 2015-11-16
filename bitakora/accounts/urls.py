from django.conf.urls import url, include, patterns

urlpatterns = patterns('',
	url(r'^$','django.contrib.auth.views.login', name='erabiltzailea_user_login'),
    url(r'^useroptions$','tokikom.views.useroptions', name='erabiltzailea_useroptions'),
    url(r'^change_pass/$','django.contrib.auth.views.password_change', name='pasahitza_aldatu'),
    (r'^accounts$', include('registration.backends.default.urls')),
    (r'', include('cssocialuser.urls')),