from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..services.transfer_game_service import start_game_for_user, guess_player

start_game_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "transfer_details": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from_club": openapi.Schema(type=openapi.TYPE_STRING),
                "to_club": openapi.Schema(type=openapi.TYPE_STRING),
                "transfer_amount": openapi.Schema(type=openapi.TYPE_NUMBER, format="float"),
            }
        ),
        "remaining_attempts": openapi.Schema(type=openapi.TYPE_INTEGER),
        "game_over": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "guessed_correctly": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "correct_player": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
    }
)

@swagger_auto_schema(
    method='get',
    operation_description="Rozpocznij dzisiejszą grę w zgadywaniu piłkarza po transferze. Zwraca szczegóły transferu (bez nazwiska poprawnego piłkarza) i liczbę pozostałych prób.",
    responses={
        200: openapi.Response(description="Szczegóły gry transferowej", schema=start_game_response_schema),
        401: openapi.Response(description="Brak autoryzacji"),
        500: openapi.Response(description="Błąd serwera"),
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def start_transfer_game(request):
    response_data = start_game_for_user(request.user)
    return Response(response_data)



guess_transfer_player_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["player_name"],
    properties={
        "player_name": openapi.Schema(type=openapi.TYPE_STRING, description="Proponowane nazwisko piłkarza"),
    }
)

guess_transfer_player_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "guessed_correctly": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "remaining_attempts": openapi.Schema(type=openapi.TYPE_INTEGER),
        "game_over": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "correct_player": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "from_club": openapi.Schema(type=openapi.TYPE_STRING),
        "to_club": openapi.Schema(type=openapi.TYPE_STRING),
        "transfer_amount": openapi.Schema(type=openapi.TYPE_NUMBER, format="float"),
    }
)

@swagger_auto_schema(
    method='post',
    operation_description="Spróbuj zgadnąć nazwisko piłkarza dla dzisiejszego transferu.",
    request_body=guess_transfer_player_request,
    responses={
        200: openapi.Response(description="Odpowiedź po zgadywaniu", schema=guess_transfer_player_response),
        400: openapi.Response(description="Brak danych lub gra nie rozpoczęta"),
        403: openapi.Response(description="Brak dostępnych prób lub już zgadnięto"),
        401: openapi.Response(description="Brak autoryzacji"),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def guess_transfer_player(request):
    player_name = request.data.get("player_name", "").strip()
    response_data = guess_player(request.user, player_name)
    return Response(response_data)
