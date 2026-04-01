from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated

from restaurants.models import Restaurant
from reviews.models import Review
from reviews.serializers import ReviewDetailSerializer, ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        return self.queryset.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id")
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        serializer.save(user=self.request.user, restaurant=restaurant)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Review.objects.get(
            id=self.kwargs.get("review_id"), user=self.request.user
        )
