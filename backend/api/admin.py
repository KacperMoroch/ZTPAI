from django.contrib import admin
from .models import Role, UserAccount, Country, League, Club, Position, Age, ShirtNumber, Player


# rejestrowanie modeli w panelu administracyjnym Django, dzięki czemu można nimi zarządzać w interfejsie admina
admin.site.register(Role)
admin.site.register(UserAccount)
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Position)
admin.site.register(Age)
admin.site.register(ShirtNumber)
admin.site.register(Player)
