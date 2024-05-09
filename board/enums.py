from django.db import models


class ColorChoices(models.TextChoices):
    DEFAULT = "DEFAULT", "DEFAULT"
    BLUE = "BLUE", "BLUE"
    RED = "RED", "RED"
    YELLOW = "YELLOW", "YELLOW"
    GREEN = "GREEN", "GREEN"
