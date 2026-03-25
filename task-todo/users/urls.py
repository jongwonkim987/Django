# users/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path

from users import cb_views

urlpatterns = [
    path('signup/', cb_views.SignupView.as_view(), name='signup'),
    path('login/', cb_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', cb_views.verify_email, name='verify_email'),
]
