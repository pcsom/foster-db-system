from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('static/js/<str:fileName>', views.java_script, name='java_script'),
]