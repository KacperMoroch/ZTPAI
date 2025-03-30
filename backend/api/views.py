from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import Player, UserAccount, Role
from .serializers import PlayerSerializer, UserAccountSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# przykładowa klasa widoku oparta na APIView.
# obsługuje tylko metodę GET i zwraca przykładowe dane użytkownika.
class ExampleView(APIView):
    def get(self, request):
        data = {
            "id": 1,
            "name": "Karol Kłos",
            "email": "karol.klos@gmail.com"
        }
        return Response(data, status=status.HTTP_200_OK)


# widok zwracający listę wszystkich użytkowników w systemie, metoda GET pobiera wszystkich użytkowników z bazy i zwraca ich w formacie JSON.
@api_view(['GET'])
def get_all_users(request):
    try:
        users = UserAccount.objects.all()  # pobranie wszystkich użytkowników z bazy
        if not users.exists():             # sprawdzenie czy lista użytkowników nie jest pusta
            return Response({"message": "Brak użytkowników w bazie"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = UserAccountSerializer(users, many=True)  # serializacja danych użytkowników
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # obsługa błędów i zwrócenie odpowiedzi serwera z kodem 500
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# widok pobierający pojedynczego użytkownika na podstawie ID, jeśli użytkownik o danym ID nie istnieje, zwracany jest błąd 404.
@api_view(['GET'])
def get_user(request, id):
    user = get_object_or_404(UserAccount, pk=id)  # pobranie użytkownika lub zwrócenie błędu 404
    serializer = UserAccountSerializer(user)      # serializacja danych użytkownika
    return Response(serializer.data, status=status.HTTP_200_OK)


# widok zwracający listę wszystkich piłkarzy w systemie, metoda GET pobiera wszystkich piłkarzy i zwraca ich w formacie JSON.
@api_view(['GET'])
def get_all_players(request):
    try:
        players = Player.objects.all()  # pobranie wszystkich piłkarzy z bazy
        if not players.exists():        # sprawdzenie czy lista piłkarzy nie jest pusta
            return Response({"message": "Brak piłkarzy w bazie"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = PlayerSerializer(players, many=True)  # serializacja danych piłkarzy
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # obsługa błędów i zwrócenie odpowiedzi serwera z kodem 500
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# widok pobierający pojedynczego piłkarza na podstawie ID, jeśli piłkarz o danym ID nie istnieje, zwracany jest błąd 404.
@api_view(['GET'])
def get_player(request, id):
    player = get_object_or_404(Player, pk=id)  # pobranie piłkarza lub zwrócenie błędu 404
    serializer = PlayerSerializer(player)      # serializacja danych piłkarza
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    login = request.data.get('login')
    password = request.data.get('password')

    if not email or not login or not password:
        return Response({"error": "Wszystkie pola są wymagane!"}, status=status.HTTP_400_BAD_REQUEST)

    # sprawdzamy czy email lub login już istnieje
    if UserAccount.objects.filter(email=email).exists():
        return Response({"error": "Użytkownik o podanym e-mailu już istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
    if UserAccount.objects.filter(login=login).exists():
        return Response({"error": "Login jest już zajęty!"}, status=status.HTTP_400_BAD_REQUEST)

    # tworzymy użytkownika
    try:
        user = UserAccount.objects.create_user(email=email, login=login, password=password)
        return Response({"message": "Użytkownik zarejestrowany pomyślnie!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": f"Błąd rejestracji: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_roles(request):
    roles = Role.objects.all()
    role_list = [{"id": role.id, "rola": role.rola} for role in roles]
    return Response(role_list, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Wszystkie pola są wymagane!"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if user is None:
        return Response({"error": "Nieprawidłowe dane logowania!"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)

    return Response({"message": "Zalogowano pomyślnie!", "token": token.key}, status=status.HTTP_200_OK)
