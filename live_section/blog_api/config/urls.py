from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from comments.views import CommentViewSet
from posts.views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("users/", include("users.urls")),
]
