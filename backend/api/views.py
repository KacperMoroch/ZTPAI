from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import Player, UserAccount
from .serializers import PlayerSerializer, UserAccountSerializer


# przykładowa klasa widoku oparta na APIView
class ExampleView(APIView):
    def get(self, request):
        data = {
            "id": 1,
            "name": "Karol Kłos",
            "email": "karol.klos@gmail.com"
        }
        return Response(data, status=status.HTTP_200_OK)


# pobieranie wszystkich użytkowników
@api_view(['GET'])
def get_all_users(request):
    try:
        users = UserAccount.objects.all()
        if not users.exists():
            return Response({"message": "Brak użytkowników w bazie"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# pobieranie użytkownika po ID
@api_view(['GET'])
def get_user(request, id):
    user = get_object_or_404(UserAccount, pk=id)
    serializer = UserAccountSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# pobieranie wszystkich piłkarzy 
@api_view(['GET'])
def get_all_players(request):
    try:
        players = Player.objects.all()
        if not players.exists():
            return Response({"message": "Brak piłkarzy w bazie"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# pobieranie piłkarza po ID
@api_view(['GET'])
def get_player(request, id):
    player = get_object_or_404(Player, pk=id)
    serializer = PlayerSerializer(player)
    return Response(serializer.data, status=status.HTTP_200_OK)

