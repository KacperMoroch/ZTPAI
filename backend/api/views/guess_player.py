from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import PlayerNameSerializer
from api.services.daily_game_service import (
    handle_player_guess,
    get_daily_game_status,
    get_player_name_suggestions
)


@swagger_auto_schema(
    method='post',
    operation_description="Sprawdź, czy odgadnięty piłkarz zgadza się z dzisiejszym.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['player_name'],
        properties={
            'player_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nazwa piłkarza')
        },
    ),
    responses={
        200: openapi.Response(description="Poprawne zgłoszenie zgadywania"),
        400: openapi.Response(description="Brak nazwy piłkarza"),
        403: openapi.Response(description="Brak prób lub już odgadnięto"),
        404: openapi.Response(description="Nie znaleziono piłkarza"),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_guess(request):
    player_name = request.data.get('player_name', '').strip()
    result = handle_player_guess(request.user, player_name)
    return Response(result['data'], status=result['status'])


@swagger_auto_schema(
    method='get',
    operation_description="Zwraca status gry użytkownika na dany dzień.",
    responses={
        200: openapi.Response(description="Status gry z liczbą pozostałych prób"),
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_game_status(request):
    data = get_daily_game_status(request.user)
    return Response(data)


@swagger_auto_schema(
    method='get',
    operation_description="Zwraca listę nazwisk piłkarzy pasujących do zapytania.",
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            description="Fragment nazwy piłkarza do wyszukania",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: openapi.Response(description="Lista pasujących piłkarzy")}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_player_names(request):
    query = request.GET.get('query', '').strip()
    names = get_player_name_suggestions(query)
    return Response({'players': names})
