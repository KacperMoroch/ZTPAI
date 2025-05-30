from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from rest_framework import status
from django.db import transaction

from ..models import Transfer, TransferQuestionOfTheDay, UserGuessLogTransfer
from ..serializers import TransferSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import date

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

    log, created = UserGuessLogTransfer.objects.get_or_create(
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



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
# @transaction.atomic
def guess_transfer_player(request):
    user = request.user
    player_name = request.data.get("player_name", "").strip()
    today = date.today()

    if not player_name:
        return Response({"error": "Brak nazwy piłkarza."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        question = TransferQuestionOfTheDay.objects.get(question_date=today)
    except TransferQuestionOfTheDay.DoesNotExist:
        return Response({"error": "Gra nie została rozpoczęta."}, status=status.HTTP_400_BAD_REQUEST)

    transfer = question.transfer
    log, _ = UserGuessLogTransfer.objects.get_or_create(
        user=user,
        guess_date=today,
        defaults={'guess_number': 0, 'guessed_correctly': False}
    )

    if log.guessed_correctly:
        return Response({
            "error": f"Już zgadłeś dzisiaj piłkarza. Spróbuj ponownie jutro. Piłkarzem do zgadnięcia był: {transfer.player.name}."
        })

    if log.guess_number >= 5:
        return Response({
            "error": f"Nie masz więcej prób. Spróbuj ponownie jutro. Piłkarzem do zgadnięcia był: {transfer.player.name}.",
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
