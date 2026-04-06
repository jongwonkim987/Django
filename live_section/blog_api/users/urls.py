from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import UserDetailView, UserSignupView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # JWT
    path("jwt/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
]
