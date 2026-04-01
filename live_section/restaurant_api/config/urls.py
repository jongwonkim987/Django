from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from restaurants.urls import router as restaurants_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include(restaurants_router.urls)),
    path("", include("reviews.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
