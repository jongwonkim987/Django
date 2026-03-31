from django.conf import settings
from django.db import models

from config.models import BaseModel
from restaurants.models import Restaurant


class Review(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.CharField(max_length=50)
    comment = models.TextField()

    def __str__(self):
        return self.title
