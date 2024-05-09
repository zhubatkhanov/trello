from django.urls import path

from board import views


urlpatterns = [
    path("board", views.BoardListCreate.as_view(), name="board"),
    path("board/<int:pk>", views.BoardDetail.as_view(), name="board detail"),
    path("column", views.ColumnListCreate.as_view(), name="column"),
    path(
        "column/<int:pk>", views.ColumnDetail.as_view(), name="column detail"
    ),
    path(
        "movecolumn/<int:pk>",
        views.MoveColumnView.as_view(),
        name="column move position",
    ),
    path("card", views.CardListCreate.as_view(), name="card"),
    path("card/<int:pk>", views.CardDetail.as_view(), name="card detail"),
]
