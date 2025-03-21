from rest_framework import serializers
from .models import Player, Role, UserAccount, Country, League, Club, Position, Age, ShirtNumber


# serializer dla pikarzy
class PlayerSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)
    league_name = serializers.CharField(source="league.name", read_only=True)
    club_name = serializers.CharField(source="club.name", read_only=True)
    position_name = serializers.CharField(source="position.name", read_only=True)
    age_value = serializers.IntegerField(source="age.value", read_only=True)
    shirt_number_value = serializers.IntegerField(source="shirt_number.number", read_only=True)


    class Meta:
        model = Player
        fields = ['id', 'name', 'country_name', 'league_name', 'club_name', 'position_name', 'age_value', 'shirt_number_value']


# serializer dla użytkowników
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

# serializer dla ról użytkowników
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# serializer dla krajów
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

# serializer dla lig
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'

# serializer dla klubów
class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

# serializer dla pozycji
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

# serializer dla wieku
class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = '__all__'

# serializer dla numerów na koszulkach
class ShirtNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShirtNumber
        fields = '__all__'
