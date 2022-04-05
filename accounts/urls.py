from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name='register'),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("change-username/<str:pk>", views.changeUsername, name="change-username"),

    path('type-of-care/<str:pk>', views.typeOfCare, name='type-of-care'),
    path('add-child/<str:pk>', views.addChild, name='add-child'),
    path('update-child/<str:pk>', views.updateChild, name='update-child'),
    path('delete-child/<str:pk>', views.deleteChild, name='delete-child'),
    path('update-basic/<str:pk>', views.updateBasic, name='update-basic'),

    path('password-reset', auth_views.PasswordResetView.as_view(template_name="passwordReset.html"), name="reset_password"),
    path('password-reset-sent', auth_views.PasswordResetDoneView.as_view(template_name="passwordResetSent.html"), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="passwordResetForm.html"), name="password_reset_confirm"),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name="passwordResetDone.html"), name="password_reset_complete"),
    #path('password-change', auth_views.PasswordChangeView.as_view(template_name="passwordChange.html"), name="password_change"),
    path('password-change', views.passwordChange, name="password-change"),
]