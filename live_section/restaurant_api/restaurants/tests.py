from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from restaurants.models import Restaurant


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant_data = {
            "name": "테스트 식당",
            "address": "서울시 강남구 테스트로 123",
            "contact": "02-1234-5678",
            "open_time": "09:00:00",
            "close_time": "22:00:00",
            "last_order": "21:30:00",
            "regular_holiday": "MON",
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_data)
        self.assertEqual(restaurant.name, self.restaurant_data["name"])
        self.assertEqual(restaurant.address, self.restaurant_data["address"])
        self.assertEqual(restaurant.contact, self.restaurant_data["contact"])
        self.assertEqual(str(restaurant.open_time), self.restaurant_data["open_time"])
        self.assertEqual(str(restaurant.close_time), self.restaurant_data["close_time"])
        self.assertEqual(str(restaurant.last_order), self.restaurant_data["last_order"])
        self.assertEqual(
            restaurant.regular_holiday, self.restaurant_data["regular_holiday"]
        )
        self.assertIsNotNone(restaurant.created_at)
        self.assertIsNotNone(restaurant.modified_at)


class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="뷰 테스트 식당",
            address="서울시 종로구 테스트로 456",
            contact="02-9999-8888",
        )
        self.list_url = reverse("restaurant-list")
        self.detail_url = reverse(
            "restaurant-detail", kwargs={"pk": self.restaurant.pk}
        )

    def test_restaurant_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_post_view(self):
        data = {
            "name": "새 식당",
            "address": "부산시 해운대구 테스트로 789",
            "contact": "051-1234-5678",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_restaurant_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.restaurant.name)

    def test_restaurant_update_view(self):
        data = {
            "name": "수정된 식당",
            "address": self.restaurant.address,
            "contact": self.restaurant.contact,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "수정된 식당")

    def test_restaurant_delete_view(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0)
