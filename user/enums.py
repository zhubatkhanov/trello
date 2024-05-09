from django.db import models


class SubscriptionChoices(models.TextChoices):
    FREE = "FREE", "FREE"
    PREMIUM = "PREMIUM", "PREMIUM"
