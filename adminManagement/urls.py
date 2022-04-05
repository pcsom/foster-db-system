from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("all-family-info", views.allFamilyInfo, name="all-family-info"),
    path("get-family-data-array", views.getFamilyDataArray, name="get-family-data-array"),
    path("update-family", views.updateFamily, name="update-family"),
    path('view-family/<str:pk>', views.viewFamily, name='view-family'),
    path('create-user', views.createUser, name='create-user'),

    path("all-child-info", views.allChildInfo, name="all-child-info"),
    path("get-child-data-array", views.getChildDataArray, name="get-child-data-array"),

    path('add-dist-entry', views.addDistLogEntry, name='add-dist-entry'),
    path('view-dist-log', views.viewDistLog, name='view-dist-log'),
    path('get-dist-data-array', views.getDistDataArray, name='get-dist-data-array'),
    path("update-dist", views.updateDist, name="update-dist"),
    path("delete-dist", views.deleteDist, name="delete-dist"),

    path('add-donor-entry', views.addDonorLogEntry, name='add-donor-entry'),
    path('view-donor-log', views.viewDonorLog, name='view-donor-log'),
    path('get-donor-data-array', views.getDonorDataArray, name='get-donor-data-array'),
    path("update-donor", views.updateDonor, name="update-donor"),
    path("delete-donor", views.deleteDonor, name="delete-donor"),
    
    path('add-hours-entry', views.addHoursLogEntry, name='add-hours-entry'),
    path('view-hours-log', views.viewHoursLog, name='view-hours-log'),
    path('get-hours-data-array', views.getHoursDataArray, name='get-hours-data-array'),
    path("update-hours", views.updateHours, name="update-hours"),
    path("delete-hours", views.deleteHours, name="delete-hours"),
    
    path('all-vol-info', views.allVolInfo, name='all-vol-info'),
    path('get-vol-data-array', views.getVolDataArray, name='get-vol-data-array'),
    path("update-vol", views.updateVol, name="update-vol"),
    path("delete-vol", views.deleteVol, name="delete-vol"),

    path("view-all-requests/<str:pk>", views.viewAllRequests, name="view-all-requests"),
    path("get-request-report/<str:pk>", views.getRequestReport, name="get-request-report"),
    path("notify-requests", views.notifyRequests, name="notify-requests"),
    path("get-user-requests", views.getUserRequests, name="get-user-requests"),
    path("request-track-info", views.requestTrackInfo, name="request-track-info"),
]