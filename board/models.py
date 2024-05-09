from django.db import models
from rest_framework.exceptions import ValidationError

from board.enums import ColorChoices
from user.models import User


class Board(models.Model):
    name = models.CharField(max_length=255, verbose_name="Board Name")
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Board Created Date"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="boards"
    )

    def save(self, *args, **kwargs):
        """Лимит на создание карточек

        Если у пользователя тип подписки бесплатная,
        у него будет лимит на создание карточек
        """
        if self.user.boards.count() >= 3 and self.user.subscription == "FREE":
            raise ValidationError(
                "Only 3 boards are allowed for FREE subscription"
            )
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_name_user"
            )
        ]

    def __str__(self):
        return f"{self.name} by user {self.user} | {self.id}"


class Column(models.Model):
    name = models.CharField(max_length=255, verbose_name="Column Name")
    color = models.CharField(
        max_length=20,
        choices=ColorChoices.choices,
        default=ColorChoices.DEFAULT,
        verbose_name="Column Color",
    )
    position = models.IntegerField()
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="columns"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_name_board"
            )
        ]

    def save(self, *args, **kwargs):
        """Лимит на изменения цвет колонок"""
        if self.board.user.subscription == "FREE" and self.color != "DEFAULT":
            raise ValidationError(
                "You cannot change the list color with a free subscription!"
            )
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name} by board {self.board}. User: {self.board.user.name}."
        )

    def move_position(self, new_position):
        """Меняет позиций карточек"""
        old_position = self.position
        self.position = new_position
        other_columns = Column.objects.filter(
            board=self.board, position__gte=new_position
        ).exclude(pk=self.pk)
        if new_position <= old_position:
            other_columns.update(position=models.F("position") + 1)
        else:
            other_columns.update(position=models.F("position") - 1)
        self.save()


class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position = models.IntegerField()
    external_link = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    column = models.ForeignKey(Column, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["column", "name"], name="unique_name_column"
            )
        ]

    def __str__(self):
        return f"{self.name} by column {self.column.name} | {self.id}"
