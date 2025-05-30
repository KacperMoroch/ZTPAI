from rest_framework import serializers
from .models import Player, Role, Transfer, TransferQuestionOfTheDay, UserAccount, Country, League, Club, Position, Age, ShirtNumber, UserGuessLog, UserGuessLogTransfer, UserPlayerAssignment
import base64

# serializer dla pikarzy
class PlayerSerializer(serializers.ModelSerializer):
    # pobieramy dane
    country_name = serializers.CharField(source="country.name", read_only=True)
    league_name = serializers.CharField(source="league.name", read_only=True)
    club_name = serializers.CharField(source="club.name", read_only=True)
    position_name = serializers.CharField(source="position.name", read_only=True)
    age_value = serializers.IntegerField(source="age.value", read_only=True)
    shirt_number_value = serializers.IntegerField(source="shirt_number.number", read_only=True)


    class Meta:
        # ten serializer bazuje na modelu Player
        model = Player
        # 'fields' określa, które pola zostaną zwrócone przez API.
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

# serializer dla przypisania użytkownika do gracza
class UserPlayerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlayerAssignment
        fields = '__all__'

# serializer dla logu zgadywania użytkownika
class UserGuessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGuessLog
        fields = '__all__'

# serializer zwracający tylko nazwe zawodnika
class PlayerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name']

class UserProfileSerializer(serializers.ModelSerializer):
    points_guess = serializers.SerializerMethodField()
    points_transfer = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ['id', 'login', 'email', 'created_at', 'points_guess', 'points_transfer', 'profile_picture']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return base64.b64encode(obj.profile_picture).decode('utf-8')
        return None

    def get_points_guess(self, obj):
        return UserGuessLog.objects.filter(user=obj, guessed_correctly=True).count()

    def get_points_transfer(self, obj):
        return UserGuessLogTransfer.objects.filter(user=obj, guessed_correctly=True).count()
    
# serializer dla transferów
class TransferSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    from_club_name = serializers.CharField(source='from_club.name', read_only=True)
    to_club_name = serializers.CharField(source='to_club.name', read_only=True)

    class Meta:
        model = Transfer
        fields = ['id', 'player', 'player_name', 'from_club', 'from_club_name', 'to_club', 'to_club_name', 'transfer_amount', 'date']

# serializer dla pytania dnia o transfer
class TransferQuestionOfTheDaySerializer(serializers.ModelSerializer):
    transfer_details = TransferSerializer(source='transfer', read_only=True)

    class Meta:
        model = TransferQuestionOfTheDay
        fields = ['id', 'transfer', 'transfer_details', 'question_date']

# serializer dla logów zgadywania transferów
class UserGuessLogTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGuessLogTransfer
        fields = '__all__'