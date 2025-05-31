from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date

from ..models import Transfer, TransferQuestionOfTheDay, UserGuessLogTransfer
from ..exceptions import (
    MissingPlayerNameException,
    GameNotStartedException,
    NoMoreAttemptsException
)

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
    user = request.user
    today = date.today()

    question, _ = TransferQuestionOfTheDay.objects.get_or_create(
        question_date=today,
        defaults={'transfer': Transfer.objects.order_by('?').first()}
    )

    transfer = question.transfer

    log, _ = UserGuessLogTransfer.objects.get_or_create(
        user=user,
        guess_date=today,
        defaults={'guess_number': 0, 'guessed_correctly': False}
    )

    remaining_attempts = max(0, 5 - log.guess_number)
    game_over = log.guessed_correctly or remaining_attempts == 0

    return Response({
        "transfer_details": {
            "from_club": transfer.from_club.name,
            "to_club": transfer.to_club.name,
            "transfer_amount": float(transfer.transfer_amount),
        },
        "remaining_attempts": remaining_attempts,
        "game_over": game_over,
        "guessed_correctly": log.guessed_correctly,
        "correct_player": transfer.player.name if game_over else None
    })


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
    user = request.user
    player_name = request.data.get("player_name", "").strip()
    today = date.today()

    if not player_name:
        raise MissingPlayerNameException()

    try:
        question = TransferQuestionOfTheDay.objects.get(question_date=today)
    except TransferQuestionOfTheDay.DoesNotExist:
        raise GameNotStartedException()

    transfer = question.transfer
    log, _ = UserGuessLogTransfer.objects.get_or_create(
        user=user,
        guess_date=today,
        defaults={'guess_number': 0, 'guessed_correctly': False}
    )

    if log.guessed_correctly:
        raise NoMoreAttemptsException(detail={
            "error": "Już zgadłeś dzisiaj piłkarza. Spróbuj jutro.",
            "correct_player": transfer.player.name,
            "game_over": True,
        })

    if log.guess_number >= 5:
        raise NoMoreAttemptsException(detail={
            "error": "Nie masz więcej prób. Spróbuj ponownie jutro.",
            "correct_player": transfer.player.name,
            "game_over": True,
            "remaining_attempts": 0
        })

    guessed_correctly = player_name.lower() == transfer.player.name.lower()
    log.guess_number += 1
    if guessed_correctly:
        log.guessed_correctly = True
    log.save()

    remaining_attempts = max(0, 5 - log.guess_number)
    game_over = guessed_correctly or remaining_attempts == 0

    response_data = {
        "guessed_correctly": guessed_correctly,
        "remaining_attempts": remaining_attempts,
        "game_over": game_over,
        "correct_player": transfer.player.name if guessed_correctly or game_over else None
    }

    if guessed_correctly or game_over:
        response_data.update({
            "from_club": transfer.from_club.name,
            "to_club": transfer.to_club.name,
            "transfer_amount": float(transfer.transfer_amount)
        })

    return Response(response_data)
