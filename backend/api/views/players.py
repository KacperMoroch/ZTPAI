from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Player
from ..serializers import PlayerSerializer
from ..exceptions import NoPlayersFoundException, PlayerNotFoundException

@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę wszystkich piłkarzy",
    responses={
        200: openapi.Response(description="Lista piłkarzy"),
        204: "Brak piłkarzy",
        500: "Błąd serwera"
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_players(request):
    players = Player.objects.all()
    if not players.exists():
        raise NoPlayersFoundException()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_description="Pobierz piłkarza po ID",
    responses={
        200: openapi.Response(description="Dane piłkarza"),
        404: "Piłkarz nie znaleziony"
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_player(request, id):
    player = Player.objects.filter(pk=id).first()
    if not player:
        raise PlayerNotFoundException()
    serializer = PlayerSerializer(player)
    return Response(serializer.data, status=status.HTTP_200_OK)
