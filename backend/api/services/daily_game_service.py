from datetime import date
from api.models import Player, UserGuessLog, UserPlayerAssignment
from api.exceptions import (
    MissingPlayerNameException,
    PlayerNotFoundException,
    NoMoreAttemptsException,
    AlreadyGuessedException
)


def get_or_assign_today_player(user):
    today = date.today()
    assignment, _ = UserPlayerAssignment.objects.get_or_create(
        user=user,
        assignment_date=today,
        defaults={'player': Player.objects.order_by('?').first()}
    )
    return assignment.player


def compare_values(val1, val2):
    if val1 < val2:
        return 'up'
    elif val1 > val2:
        return 'down'
    else:
        return 'equal'


def handle_player_guess(user, player_name):
    if not player_name:
        raise MissingPlayerNameException()

    today = date.today()
    target_player = get_or_assign_today_player(user)

    try:
        guessed_player = Player.objects.select_related(
            'country', 'league', 'club', 'position', 'age', 'shirt_number'
        ).get(name=player_name)
    except Player.DoesNotExist:
        guess_log, _ = UserGuessLog.objects.get_or_create(user=user, guess_date=today)
        guess_log.guess_number += 1
        guess_log.save()

        remaining_attempts = max(0, 5 - guess_log.guess_number)
        game_over = remaining_attempts == 0
        return {
            'status': 404,
            'data': {
                'error': f"Skończyły Ci się próby na dzisiaj. Gra zakończona. Szukanym piłkarzem był: {target_player.name}." if game_over else 'Nie znaleziono piłkarza.',
                'remaining_attempts': remaining_attempts,
                'game_over': game_over
            }
        }

    guess_log, _ = UserGuessLog.objects.get_or_create(user=user, guess_date=today)

    if guess_log.guessed_correctly:
        raise AlreadyGuessedException(detail=f"Już zgadłeś. Piłkarz to: {target_player.name}.")

    if guess_log.guess_number >= 5:
        raise NoMoreAttemptsException(detail=f"Brak prób. Piłkarz to: {target_player.name}.")

    guess_log.guess_number += 1

    match_dict = {
        'country': guessed_player.country.name == target_player.country.name,
        'league': guessed_player.league.name == target_player.league.name,
        'club': guessed_player.club.name == target_player.club.name,
        'position': guessed_player.position.name == target_player.position.name,
        'age': guessed_player.age.value == target_player.age.value,
        'shirt_number': guessed_player.shirt_number.number == target_player.shirt_number.number,
        'age_comparison': compare_values(guessed_player.age.value, target_player.age.value),
        'shirt_number_comparison': compare_values(guessed_player.shirt_number.number, target_player.shirt_number.number)
    }

    game_over = all(match_dict.values())
    if game_over:
        guess_log.guessed_correctly = True

    guess_log.save()
    remaining_attempts = max(0, 5 - guess_log.guess_number)
    game_over_due_to_attempts = remaining_attempts == 0 and not game_over

    return {
        'status': 200,
        'data': {
            'correct': game_over,
            'remaining_attempts': remaining_attempts,
            'player_data': {
                'name': guessed_player.name,
                'country': guessed_player.country.name,
                'league': guessed_player.league.name,
                'club': guessed_player.club.name,
                'position': guessed_player.position.name,
                'age': guessed_player.age.value,
                'number': guessed_player.shirt_number.number,
            },
            'matches': match_dict,
            'message': (
                f"Brawo! Zgadłeś! Szukanym piłkarzem był: {target_player.name}." if game_over else (
                    f"Skończyły Ci się próby na dzisiaj. Gra zakończona. Szukanym piłkarzem był: {target_player.name}." if game_over_due_to_attempts else "Spróbuj ponownie."
                )
            ),
            'game_over': game_over or game_over_due_to_attempts
        }
    }


def get_daily_game_status(user):
    today = date.today()
    guess_log, _ = UserGuessLog.objects.get_or_create(user=user, guess_date=today)
    remaining_attempts = max(0, 5 - guess_log.guess_number)
    guessed_correctly = guess_log.guessed_correctly
    game_over = remaining_attempts == 0

    target_player = get_or_assign_today_player(user)

    data = {
        'remaining_attempts': remaining_attempts,
        'guessed_correctly': guessed_correctly,
        'game_over_due_to_attempts': game_over
    }

    # Ujawniam target_player_name tylko jeśli gra się zakończyła
    if guessed_correctly or game_over:
        data['target_player_name'] = target_player.name

    return data


def get_player_name_suggestions(query):
    if query:
        players = Player.objects.filter(name__istartswith=query)[:10]
    else:
        players = Player.objects.order_by('?')[:10]
    return [player.name for player in players]
