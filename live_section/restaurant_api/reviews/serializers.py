from rest_framework import serializers

from restaurants.serializers import RestaurantSerializer
from reviews.models import Review
from users.serializers import UserDetailSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id", "restaurant"]


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
