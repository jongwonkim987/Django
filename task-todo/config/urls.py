"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),  # Summernote 파일 업로드 URL
    path('todo/', include('todo.urls')),
    # path('accounts/', include('users.urls')),  # 기존 accounts/ 주석 처리
    path('users/', include('users.urls')),        # 새로운 users/ 엔드포인트
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 개발환경 미디어 파일 서빙
