from rest_framework import serializers
from rest_framework.validators import ValidationError

from board.models import Board, Card, Column


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "name", "created_date", "user")


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ("id", "name", "color", "position", "board", "updated_at")
        extra_kwargs = {
            "position": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        """Проверка пользователя

        Пользователь 1 не имеет доступ к доске Пользователя 2
        """
        request = self.context.get("request")
        board = attrs["board"]
        if board.user != request.user:
            raise ValidationError(
                "You do not have permission to create a column in this board."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        """При создании колонок автоматический присваиваем позицию"""
        max_position = Column.objects.count()
        validated_data["position"] = max_position + 1
        return super().create(validated_data)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            "id",
            "name",
            "description",
            "position",
            "column",
            "external_link",
            "updated_at",
        )
        extra_kwargs = {
            "position": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        """Проверка пользователя

        Пользователь 1 не имеет доступ к доске Пользователя 2
        """
        request = self.context.get("request")
        column = attrs["column"]
        if column.board.user != request.user:
            raise ValidationError(
                "You do not have permission to create a card in this column."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        """При создании карточек автоматический присваиваем позицию"""
        max_position = Card.objects.count()
        validated_data["position"] = max_position + 1
        return super().create(validated_data)
