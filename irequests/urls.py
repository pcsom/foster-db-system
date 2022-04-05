from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("new-request", views.newRequest, name="new-request"),
    path("view-requests/<str:pk>", views.viewRequests, name="view-requests"),
    path("receiving", views.receiving, name="receiving"),
]