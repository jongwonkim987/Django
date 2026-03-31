from django.db import models

from config.models import BaseModel


DAYS_OF_WEEK = [
    ("MON", "Monday"),
    ("TUE", "Tuesday"),
    ("WED", "Wednesday"),
    ("THU", "Thursday"),
    ("FRI", "Friday"),
    ("SAT", "Saturday"),
    ("SUN", "Sunday"),
]


class Restaurant(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    last_order = models.TimeField(null=True, blank=True)
    regular_holiday = models.CharField(
        max_length=3,
        choices=DAYS_OF_WEEK,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
