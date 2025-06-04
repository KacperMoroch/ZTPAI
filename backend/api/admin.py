from django.contrib import admin
from .models import (
    Role,
    UserAccount,
    Country,
    League,
    Club,
    Position,
    Age,
    ShirtNumber,
    Player,
    UserGuessLog,
    UserPlayerAssignment,
    Transfer,
    TransferQuestionOfTheDay,
    UserGuessLogTransfer,
)

# Rejestrowanie modeli w panelu administracyjnym Django
admin.site.register(Role)
admin.site.register(UserAccount)
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Position)
admin.site.register(Age)
admin.site.register(ShirtNumber)
admin.site.register(Player)
admin.site.register(UserPlayerAssignment)
admin.site.register(UserGuessLog)
admin.site.register(Transfer)
admin.site.register(TransferQuestionOfTheDay)
admin.site.register(UserGuessLogTransfer)
