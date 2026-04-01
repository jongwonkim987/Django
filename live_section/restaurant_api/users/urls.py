from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserDetailView, UserLoginView, UserSignupView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
