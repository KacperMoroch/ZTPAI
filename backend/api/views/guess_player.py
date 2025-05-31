from datetime import date 
from django.db.models import F
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import PlayerNameSerializer
from api.models import *
from api.exceptions import (
    MissingPlayerNameException,
    PlayerNotFoundException,
    NoMoreAttemptsException,
    AlreadyGuessedException
)

def get_or_assign_today_player(user):
    today = date.today()
    assignment, created = UserPlayerAssignment.objects.get_or_create(
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
    if not player_name:
        raise MissingPlayerNameException()

    user = request.user
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
        game_over_due_to_attempts = remaining_attempts == 0

        if game_over_due_to_attempts:
            return Response({   
                'error': f"Skończyły Ci się próby na dzisiaj. Gra zakończona. Szukanym piłkarzem był: {target_player.name}.",
                'remaining_attempts': remaining_attempts,
                'game_over': game_over_due_to_attempts
            }, status=404)             
        return Response({
                'error': 'Nie znaleziono piłkarza.',
                'remaining_attempts': remaining_attempts,
                'game_over': game_over_due_to_attempts
            }, status=404)
    

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

    return Response({
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
    })




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

    if query:
        players = Player.objects.filter(name__istartswith=query)[:10]
    else:
        players = Player.objects.order_by('?')[:10]

    serializer = PlayerNameSerializer(players, many=True)
    return Response({'players': [p['name'] for p in serializer.data]})




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
    user = request.user
    today = date.today()
    guess_log, _ = UserGuessLog.objects.get_or_create(user=user, guess_date=today)
    remaining_attempts = max(0, 5 - guess_log.guess_number)
    guessed_correctly = guess_log.guessed_correctly
    game_over_due_to_attempts = remaining_attempts == 0

    target_player = get_or_assign_today_player(user)

    response_data = {
        'remaining_attempts': remaining_attempts,
        'guessed_correctly': guessed_correctly,
        'game_over_due_to_attempts': game_over_due_to_attempts,
    }

    # Ujawniam target_player_name tylko jeśli gra się zakończyła
    if guessed_correctly or game_over_due_to_attempts:
        response_data['target_player_name'] = target_player.name

    return Response(response_data)
