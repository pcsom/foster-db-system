from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('oauth2callback', views.OAuth2CallBack, name='oauth2callback'),
    path('auth-account', views.authAccount, name='auth-account'),
    path('static/js/<str:fileName>', views.java_script, name='java_script'),
]