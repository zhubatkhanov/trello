from django.contrib import admin

from board.models import Board, Card, Column


admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Card)
