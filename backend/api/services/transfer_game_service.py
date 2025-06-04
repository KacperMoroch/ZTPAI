from datetime import date
from ..models import Transfer, TransferQuestionOfTheDay, UserGuessLogTransfer
from ..exceptions import (
    MissingPlayerNameException,
    GameNotStartedException,
    NoMoreAttemptsException
)

def start_game_for_user(user):
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

    return {
        "transfer_details": {
            "from_club": transfer.from_club.name,
            "to_club": transfer.to_club.name,
            "transfer_amount": float(transfer.transfer_amount),
        },
        "remaining_attempts": remaining_attempts,
        "game_over": game_over,
        "guessed_correctly": log.guessed_correctly,
        "correct_player": transfer.player.name if game_over else None
    }


def guess_player(user, player_name):
    if not player_name:
        raise MissingPlayerNameException()

    today = date.today()

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

    return response_data
