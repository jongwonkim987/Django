from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurants.models import Restaurant
from reviews.models import Review

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reviewer@example.com",
            nickname="reviewer",
            password="reviewpass123",
        )
        self.restaurant = Restaurant.objects.create(
            name="리뷰 테스트 식당",
            address="서울시 마포구 테스트로 101",
            contact="02-5555-6666",
        )

    def test_create_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title="맛있는 식당",
            comment="음식이 정말 맛있었습니다. 다음에 또 방문하고 싶어요.",
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(review.title, "맛있는 식당")
        self.assertEqual(
            review.comment, "음식이 정말 맛있었습니다. 다음에 또 방문하고 싶어요."
        )
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.modified_at)
