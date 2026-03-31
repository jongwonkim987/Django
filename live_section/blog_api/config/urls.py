"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet  # posts 앱의 ViewSet 임포트

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")  # basename 지정 베스트 프랙티스

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),  # 세션 1에서 추가된 부분 유지
    path("api/", include(router.urls)),  # router URL 통합, 모듈화 베스트 프랙티스
]
