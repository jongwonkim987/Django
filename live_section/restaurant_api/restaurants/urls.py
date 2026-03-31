from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewSet

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurant")

urlpatterns = router.urls
