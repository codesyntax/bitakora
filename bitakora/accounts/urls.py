from django.conf.urls import url, include
from django.contrib.auth.views import LoginView
from bitakora.accounts.views import BlogPasswordChangeView
from tokikom import views

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='erabiltzailea_user_login'),
    url(r'^useroptions$', views.useroptions, name='erabiltzailea_useroptions'),
    url(r'^change_pass/$', BlogPasswordChangeView.as_view(), name='pasahitza_aldatu'),
    url(r'^accounts$', include('registration.backends.default.urls')),
    url(r'', include('cssocialuser.urls')),
]