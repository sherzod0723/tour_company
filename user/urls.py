from django.urls import path
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path('register/', SignupView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset_confirm/', ResetPasswordForm.as_view(), name='reset_confirm'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate'),
    path('reset_password/<str:uidb64>/<str:token>', reset_password, name='reset_password'),
]