from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("login/jwt/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("signup/", views.UserSignupView.as_view(), name="user-signup"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("profile/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
]
