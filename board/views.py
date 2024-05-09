from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import Board, Card, Column
from board.serializers import BoardSerializer, CardSerializer, ColumnSerializer
from user.renderers import UserRenderer


class BoardListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращаем board list доступные к пользователю"""
        boards = Board.objects.filter(user=request.user.id)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание новой доски"""
        request.data["user"] = request.user.id
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BoardDetail(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, pk):
        """Возвращаем board, если у user есть доступ"""
        board = Board.objects.filter(pk=pk, user=self.request.user).first()
        if board is not None:
            return board
        raise PermissionDenied(
            "Column not found or you don't have permission to access it"
        )

    def get(self, request, pk):
        """Возвращем board по id"""
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk):
        """Редактируем board по id"""
        board = self.get_object(pk)
        request.data["user"] = request.user.id
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление board"""
        board = self.get_object(pk)
        board.delete()
        return Response(
            {"message": "delete success"}, status=status.HTTP_204_NO_CONTENT
        )


class ColumnListCreate(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request):
        """Возвращаем board list доступные к пользователю

        Через board_id возвращаем конкретную колонку
        http://127.0.0.1/api/v1/columns?board=1
        """
        board_id = request.query_params.get("board", None)
        if board_id is not None:
            columns = Column.objects.filter(
                board__id=board_id, board__user=request.user
            )
        else:
            columns = Column.objects.filter(board__user=request.user)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание новой колонки"""
        serializer = ColumnSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ColumnDetail(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, pk):
        """Возвращаем object, если у user есть доступ"""
        column = Column.objects.filter(
            pk=pk, board__user=self.request.user
        ).first()
        if column is not None:
            return column
        raise PermissionDenied(
            "Column not found or you don't have permission to access it"
        )

    def get(self, request, pk):
        """Возвращем column по id"""
        column = self.get_object(pk)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)

    def put(self, request, pk):
        """Редактируем column по id"""
        column = self.get_object(pk)
        serializer = ColumnSerializer(
            column, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление column"""
        column = self.get_object(pk)
        column.delete()
        return Response(
            {"message": "delete success"}, status=status.HTTP_204_NO_CONTENT
        )


class MoveColumnView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        column = Column.objects.filter(pk=pk).first()
        if column is not None:
            return column
        raise PermissionDenied(
            "Column not found or you don't have permission to access it"
        )

    def post(self, request, pk):
        """Для изменения позиций колонок"""
        column = self.get_object(pk=pk)
        new_position = request.data.get("position", None)
        if new_position is None:
            return Response(
                {"error": "New position is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        column.move_position(new_position)
        return Response(
            {"message": "Column moved successfully"}, status=status.HTTP_200_OK
        )


class CardListCreate(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request):
        """Возвращаем card list доступные к пользователю

        Через card_id возвращаем конкретную колонку
        http://127.0.0.1/api/v1/columns?card=1
        """
        column_id = request.query_params.get("column", None)
        if column_id is None:
            cards = Card.objects.filter(column__board__user=request.user)
        else:
            cards = Card.objects.filter(
                column__id=column_id, column__board__user=request.user
            )
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание новой карточки"""
        serializer = CardSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CardDetail(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, pk):
        """Возвращаем object, если у user есть доступ"""
        card = Card.objects.filter(
            pk=pk, column__board__user=self.request.user
        ).first()
        if card is not None:
            return card
        raise PermissionDenied(
            "Column not found or you don't have permission to access it"
        )

    def get(self, request, pk):
        """Возвращем card по id"""
        card = self.get_object(pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)

    def put(self, request, pk):
        """Редактируем card по id"""
        card = self.get_object(pk)
        serializer = CardSerializer(
            card, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление card по id"""
        card = self.get_object(pk)
        card.delete()
        return Response(
            {"message": "delete success"}, status=status.HTTP_204_NO_CONTENT
        )
