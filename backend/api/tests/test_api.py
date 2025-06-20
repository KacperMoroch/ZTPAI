import pytest
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from django.urls import reverse
from api.services.daily_game_service import compare_values, get_or_assign_today_player
from api.views.players import get_all_players, get_player, get_unique_filters

from api.views.example import ExampleView
from api.models import Age, Club, Country, League, Position, ShirtNumber, Transfer, TransferQuestionOfTheDay, UserAccount, Player, Role,  UserGuessLog, UserGuessLogTransfer, UserPlayerAssignment
import base64
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock, patch
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from decimal import Decimal

# Fixture inicjalizujący niezalogowanego klienta API
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def user(db):
    return UserAccount.objects.create_user(
        email='testuser123@example.com',
        login='testuser123',
        password='testpass123'
    )
# Fixture tworzący superużytkownika, logujący go i ustawiający token JWT
@pytest.fixture
def auth_client(client):
    # Tworzymy superużytkownika
    user = UserAccount.objects.create_user(
        email="testuser@example.com",
        login="testuser",
        password="testpassword",
        is_superuser=True
    )
    # Logowanie użytkownika
    response = client.post('/api/login/', {
        "email": "testuser@example.com",
        "password": "testpassword"
    }, format='json')

    # Sprawdzenie poprawności logowania
    assert response.status_code == 200, f"Login failed: {response.data}"

    # Ustawienie tokena w nagłówkach klienta
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client

@pytest.fixture
def transfer_question(db):
    # Tworzymy zależne obiekty wymagane przez Player
    country = Country.objects.create(name="Poland")
    league = League.objects.create(name="Ekstraklasa")
    club_from = Club.objects.create(name="Club From")
    club_to = Club.objects.create(name="Club To")
    position = Position.objects.create(name="Forward")
    age = Age.objects.create(value=25)
    shirt_number = ShirtNumber.objects.create(number=10)

    # Tworzymy Player z kompletem wymaganych FK
    player = Player.objects.create(
        name="Test Player",
        country=country,
        league=league,
        club=club_from,
        position=position,
        age=age,
        shirt_number=shirt_number,
    )

    transfer = Transfer.objects.create(
        player=player,
        from_club=club_from,
        to_club=club_to,
        transfer_amount=10_000_000,
        date=date.today()
    )

    question = TransferQuestionOfTheDay.objects.create(
        transfer=transfer,
        question_date=date.today()
    )
    return question



@pytest.fixture
def assign_target_player(user, target_player):
    # Przypisujemy target_player do user na dzisiaj
    return UserPlayerAssignment.objects.create(user=user, assignment_date=date.today(), player=target_player)



@pytest.fixture
def player_data(db):
    country = Country.objects.create(name="Poland")
    league = League.objects.create(name="Ekstraklasa")
    club = Club.objects.create(name="Club")
    position = Position.objects.create(name="Forward")
    age = Age.objects.create(value=25)
    shirt_number = ShirtNumber.objects.create(number=10)
    return {
        "country": country,
        "league": league,
        "club": club,
        "position": position,
        "age": age,
        "shirt_number": shirt_number,
    }

@pytest.fixture
def target_player(db, player_data):
    return Player.objects.create(
        name="Target Player",
        country=player_data["country"],
        league=player_data["league"],
        club=player_data["club"],
        position=player_data["position"],
        age=player_data["age"],
        shirt_number=player_data["shirt_number"],
    )

@pytest.fixture
def guessed_player(db, player_data):
    return Player.objects.create(
        name="Guessed Player",
        country=player_data["country"],
        league=player_data["league"],
        club=player_data["club"],
        position=player_data["position"],
        age=player_data["age"],
        shirt_number=player_data["shirt_number"],
    )


@pytest.fixture
def user_auth_client(client, user):
    user.set_password('testpass123')
    user.save()

    response = client.post('/api/login/', {
        "email": user.email,
        "password": "testpass123"
    }, format='json')

    assert response.status_code == 200, f"Login failed: {response.data}"

    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client

@pytest.fixture
def club_a(db):
    return Club.objects.create(name="Club A")

@pytest.fixture
def club_b(db):
    return Club.objects.create(name="Club B")

@pytest.fixture
def player(db, club_a, player_data):
    return Player.objects.create(
        name="Test Player",
        country=player_data["country"],
        league=player_data["league"],
        club=club_a, 
        position=player_data["position"],
        age=player_data["age"],
        shirt_number=player_data["shirt_number"],
    )

@pytest.fixture
def transfer(db, player, club_a, club_b):
    return Transfer.objects.create(
        player=player,
        from_club=club_a,
        to_club=club_b,
        transfer_amount=Decimal("12.50"),
        date=date.today()
    )


# ======================= TESTY =======================



def test_example_view_get():
    factory = APIRequestFactory()
    request = factory.get('/fake-url/')  

    view = ExampleView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data["id"] == 1
    assert response.data["name"] == "Karol Kłos"
    assert response.data["email"] == "karol.klos@gmail.com"

def test_example_view_returns_200():
    request = APIRequestFactory().get('/fake-url/')
    response = ExampleView.as_view()(request)

    assert response.status_code == 200

def test_example_view_returns_correct_data():
    request = APIRequestFactory().get('/fake-url/')
    response = ExampleView.as_view()(request)

    expected_data = {
        "id": 1,
        "name": "Karol Kłos",
        "email": "karol.klos@gmail.com"
    }

    assert response.data == expected_data

def test_example_view_data_types():
    request = APIRequestFactory().get('/fake-url/')
    response = ExampleView.as_view()(request)

    assert isinstance(response.data["id"], int)
    assert isinstance(response.data["name"], str)
    assert isinstance(response.data["email"], str)

def test_example_view_does_not_return_extra_fields():
    request = APIRequestFactory().get('/fake-url/')
    response = ExampleView.as_view()(request)

    assert set(response.data.keys()) == {"id", "name", "email"}

def test_compare_values_up():
    assert compare_values(1, 2) == 'up'

def test_compare_values_down():
    assert compare_values(5, 3) == 'down'

def test_compare_values_equal():
    assert compare_values(7, 7) == 'equal'

@patch('api.models.Player.objects.order_by')
@patch('api.models.UserPlayerAssignment.objects.get_or_create')
def test_get_or_assign_today_player_creates_assignment(mock_get_or_create, mock_order_by):
    mock_user = MagicMock()
    mock_player = MagicMock()
    mock_order_by.return_value.first.return_value = mock_player
    mock_get_or_create.return_value = (MagicMock(player=mock_player), True)

    result = get_or_assign_today_player(mock_user)
    assert result == mock_player

@patch('api.models.Player.objects.order_by')
@patch('api.models.UserPlayerAssignment.objects.get_or_create')
def test_get_or_assign_today_player_creates_assignment(mock_get_or_create, mock_order_by):
    mock_user = MagicMock()
    mock_player = MagicMock()
    mock_order_by.return_value.first.return_value = mock_player
    mock_assignment = MagicMock(player=mock_player)
    mock_get_or_create.return_value = (mock_assignment, True)

    result = get_or_assign_today_player(mock_user)

    mock_order_by.assert_called_once_with('?')
    assert result == mock_player

@patch('api.models.Player.objects.order_by')
@patch('api.models.UserPlayerAssignment.objects.get_or_create')
def test_get_or_assign_today_player_assignment_already_exists(mock_get_or_create, mock_order_by):
    mock_user = MagicMock()
    mock_player = MagicMock()
    mock_assignment = MagicMock(player=mock_player)
    mock_get_or_create.return_value = (mock_assignment, False)

    result = get_or_assign_today_player(mock_user)

    assert result == mock_player

@pytest.mark.django_db
@patch('api.models.UserPlayerAssignment.objects.get_or_create')
def test_get_or_assign_today_player_returns_correct_player(mock_get_or_create):
    mock_user = MagicMock()
    mock_player = MagicMock()
    mock_assignment = MagicMock(player=mock_player)
    mock_get_or_create.return_value = (mock_assignment, False)

    result = get_or_assign_today_player(mock_user)

    assert result == mock_player

@patch('api.models.Player.objects.order_by')
@patch('api.models.UserPlayerAssignment.objects.get_or_create')
def test_get_or_assign_today_player_orders_by_random(mock_get_or_create, mock_order_by):
    mock_user = MagicMock()
    mock_player = MagicMock()
    mock_order_by.return_value.first.return_value = mock_player
    mock_assignment = MagicMock(player=mock_player)
    mock_get_or_create.return_value = (mock_assignment, True)

    result = get_or_assign_today_player(mock_user)

    mock_order_by.assert_called_once_with('?')
    mock_order_by.return_value.first.assert_called_once()
    assert result == mock_player

@patch('api.models.Player.objects')
def test_get_all_players_default_sort(mock_player_objects, api_factory, user):
    mock_qs = MagicMock()
    mock_player_objects.filter.return_value.order_by.return_value = mock_qs
    mock_qs.__len__.return_value = 0  # zero wyników

    request = api_factory.get('/players')
    force_authenticate(request, user=user)

    response = get_all_players(request)

    assert response.status_code == 200
    assert 'results' in response.data  # paginacja DRF
    mock_player_objects.filter.assert_called_once()
    mock_player_objects.filter.return_value.order_by.assert_called_with('name')


@patch('api.models.Player.objects')
def test_get_all_players_with_filters_and_sort(mock_player_objects, api_factory, user):
    mock_qs = MagicMock()
    mock_player_objects.filter.return_value.order_by.return_value = mock_qs

    request = api_factory.get('/players', {'country': 'Poland', 'league': 'Ekstraklasa', 'position': 'Defender', 'sort': '-name'})
    force_authenticate(request, user=user)

    get_all_players(request)

    mock_player_objects.filter.assert_called()
    args, kwargs = mock_player_objects.filter.call_args
    # sprawdzamy czy filtr zawiera country, league i position
    assert 'country__name__icontains' in str(args[0])
    assert 'league__name__icontains' in str(args[0])
    assert 'position__name__icontains' in str(args[0])
    mock_player_objects.filter.return_value.order_by.assert_called_with('-name')

@patch('api.serializers.PlayerSerializer')
def test_get_player_found(mock_serializer, api_factory, user):
    mock_player = MagicMock()
    with patch('api.models.Player.objects.filter') as mock_filter:
        mock_filter.return_value.first.return_value = mock_player
        mock_serializer.return_value.data = {'id': 1, 'name': 'Test Player'}

        request = api_factory.get('/players/1')
        force_authenticate(request, user=user)

        response = get_player(request, id=1)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == 1


def test_get_player_not_found(api_factory, user):
    with patch('api.views.Player.objects.filter') as mock_filter:
        mock_filter.return_value.first.return_value = None

        request = api_factory.get('/players/999')
        force_authenticate(request, user=user)

        from api.exceptions import PlayerNotFoundException

        with pytest.raises(PlayerNotFoundException):
            get_player(request, id=999)

@patch('api.views.Player.objects')
def test_get_unique_filters(api_factory, user, mock_player_objects):
    mock_player_objects.values_list.side_effect = [
        ['Poland', 'Germany', None, 'France'],
        ['Ekstraklasa', 'Bundesliga', 'La Liga', None],
        ['Forward', 'Midfielder', 'Defender', None],
    ]

    request = api_factory.get('/players/filters')
    force_authenticate(request, user=user)

    response = get_unique_filters(request)

    assert response.status_code == 200
    assert 'countries' in response.data
    assert 'leagues' in response.data
    assert 'positions' in response.data
    # powinno być odfiltrowane i wyniki posortowane
    assert response.data['countries'] == ['France', 'Germany', 'Poland']
    assert response.data['leagues'] == ['Bundesliga', 'Ekstraklasa', 'La Liga']
    assert response.data['positions'] == ['Defender', 'Forward', 'Midfielder']

@pytest.mark.django_db
def test_useraccount_clean_valid_login():
    user = UserAccount(email='test@example.com', login='abcd')
    user.clean()

@pytest.mark.django_db
def test_useraccount_clean_invalid_login():
    user = UserAccount(email='test@example.com', login='ab')
    with pytest.raises(ValidationError) as exc:
        user.clean()
    assert "co najmniej 4 znaki" in str(exc.value)

@pytest.mark.django_db
def test_user_str_returns_login():
    user = UserAccount(email='test@example.com', login='testuser')
    assert str(user) == 'testuser'

@pytest.mark.django_db
def test_role_str():
    role = Role.objects.create(rola="Admin")
    assert str(role) == "Admin"

@pytest.mark.django_db
def test_country_str():
    country = Country.objects.create(name="Polska")
    assert str(country) == "Polska"

@pytest.mark.django_db
def test_create_user_and_superuser():
    user = UserAccount.objects.create_user(email="u@a.pl", login="user", password="123")
    superuser = UserAccount.objects.create_superuser(email="admin@a.pl", login="admin", password="123")
    assert user.is_superuser is False
    assert superuser.is_superuser is True

@pytest.mark.django_db
def test_player_str_representation():
    country = Country.objects.create(name="Hiszpania")
    league = League.objects.create(name="La Liga")
    club = Club.objects.create(name="Real Madrid")
    position = Position.objects.create(name="Napastnik")
    age = Age.objects.create(value=25)
    shirt = ShirtNumber.objects.create(number=7)

    player = Player.objects.create(
        name="Cristiano Ronaldo",
        country=country,
        league=league,
        club=club,
        position=position,
        age=age,
        shirt_number=shirt
    )

    assert str(player) == "Cristiano Ronaldo"

@pytest.mark.django_db
def test_superuser_flags():
    superuser = UserAccount.objects.create_superuser("admin@a.pl", "admin", "pass")
    assert superuser.is_staff is True
    assert superuser.is_superuser is True

@pytest.mark.django_db
def test_user_guess_log_creation(user):
    log = UserGuessLog.objects.create(
        user=user,
        guess_date=date.today(),
        guess_number=2,
        guessed_correctly=True
    )
    assert log.guess_number == 2
    assert log.guessed_correctly is True
    assert log.user == user

@pytest.mark.django_db
def test_transfer_str_representation(player, club_a, club_b):
    transfer = Transfer.objects.create(
        player=player,
        from_club=club_a,
        to_club=club_b,
        transfer_amount=Decimal("12.50"),
        date=date.today()
    )
    expected = f"{player.name}: {club_a.name} ➜ {club_b.name} (12.50M)"
    assert str(transfer) == expected

@pytest.mark.django_db
def test_transfer_question_str_representation(transfer):
    q = TransferQuestionOfTheDay.objects.create(
        transfer=transfer,
        question_date=date.today()
    )
    assert str(q).startswith("Pytanie dnia: ")
    assert str(q).endswith(str(q.transfer))

@pytest.mark.django_db
def test_user_guess_log_transfer_str_and_uniqueness(user):
    log = UserGuessLogTransfer.objects.create(
        user=user,
        guess_date=date.today(),
        guess_number=1,
        guessed_correctly=False
    )
    assert "✘" in str(log)

    with pytest.raises(Exception):
        # próba stworzenia drugiego logu tego samego dnia dla tego samego użytkownika
        UserGuessLogTransfer.objects.create(
            user=user,
            guess_date=date.today(),
            guess_number=2,
            guessed_correctly=True
        )


#==========================================================================================================================================


# Testuje działanie przykładowego endpointu — czy zwraca dane o Karolu Kłosie
@pytest.mark.django_db
def test_example_view(auth_client):
    response = auth_client.get('/api/example/')
    assert response.status_code == 200
    assert response.data["name"] == "Karol Kłos"

# Test: lista użytkowników, gdy w bazie nie ma nikogo poza testuserem — oczekiwany status 200
@pytest.mark.django_db
def test_get_all_users_empty(auth_client):
    UserAccount.objects.exclude(email='testuser@example.com').delete()  
    response = auth_client.get('/api/users/')
    assert response.status_code == 200

# Test: lista użytkowników, gdy w bazie jest przynajmniej jeden — sprawdza, czy zwróci listę
@pytest.mark.django_db
def test_get_all_users_with_data(auth_client):
    UserAccount.objects.create_user(email="test@example.com", login="innylogin", password="haslo123")
    response = auth_client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data, list)

# Test: pobieranie konkretnego użytkownika po jego ID — sprawdzenie poprawności danych
@pytest.mark.django_db
def test_get_user_valid(auth_client):
    user = UserAccount.objects.create_user(email="jan@example.com", login="janek", password="haslo123")
    response = auth_client.get(f'/api/users/{user.id}/')
    assert response.status_code == 200
    assert response.data["email"] == "jan@example.com"

# Test: próba pobrania użytkownika, który nie istnieje — powinien zwrócić 404
@pytest.mark.django_db
def test_get_user_not_found(auth_client):
    response = auth_client.get('/api/users/999/')
    assert response.status_code == 404

# Test: pobieranie listy graczy, gdy baza jest pusta — oczekiwany status 200
@pytest.mark.django_db
def test_get_all_players_empty(auth_client):
    response = auth_client.get('/api/players/')
    assert response.status_code == 200
    assert response.data['results'] == []

# Test: próba pobrania nieistniejącego gracza — oczekiwany status 404
@pytest.mark.django_db
def test_get_player_not_found(auth_client):
    response = auth_client.get('/api/players/999/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_player_by_id(auth_client, target_player):
    response = auth_client.get(f'/api/players/{target_player.id}/')
    assert response.status_code == 200
    assert response.data["id"] == target_player.id
    assert response.data["name"] == target_player.name



@pytest.mark.django_db
def test_get_unique_filters(auth_client, target_player):
    response = auth_client.get('/api/filters/')
    assert response.status_code == 200

    data = response.data
    assert "countries" in data
    assert "leagues" in data
    assert "positions" in data

    assert target_player.country.name in data["countries"]
    assert target_player.league.name in data["leagues"]
    assert target_player.position.name in data["positions"]

@pytest.mark.django_db
def test_get_all_players_with_filters_and_sort(auth_client, target_player):
    response = auth_client.get('/api/players/?country=Poland&sort=name')
    assert response.status_code == 200
    results = response.data["results"]
    assert any(p["id"] == target_player.id for p in results)


@pytest.mark.django_db
def test_players_pagination(auth_client, player_data):
    # Tworzymy 5 graczy, a page_size = 3, więc będzie 2 strony
    for i in range(5):
        Player.objects.create(
            name=f"Player {i}",
            country=player_data["country"],
            league=player_data["league"],
            club=player_data["club"],
            position=player_data["position"],
            age=player_data["age"],
            shirt_number=player_data["shirt_number"],
        )

    response = auth_client.get('/api/players/?page=1')
    assert response.status_code == 200
    assert len(response.data["results"]) <= 3

    response2 = auth_client.get('/api/players/?page=2')
    assert response2.status_code == 200
    assert len(response2.data["results"]) <= 3

# Test: poprawna rejestracja nowego użytkownika — powinno zwrócić 201
@pytest.mark.django_db
def test_register_user_success(client):
    payload = {
        "email": "nowy_uzytkownik@example.com",
        "login": "nowy_uzytkownik",
        "password": "haslo123"
    }
    response = client.post('/api/register/', payload, format='json')
    assert response.status_code == 201

# Test: próba rejestracji z brakującymi danymi — powinien zwrócić błąd 400
@pytest.mark.django_db
def test_register_user_missing_fields(client):
    response = client.post('/api/register/', {"email": "brak@example.com"}, format='json')
    assert response.status_code == 400

# Test: próba rejestracji z już istniejącym adresem e-mail — powinno zwrócić 400
@pytest.mark.django_db
def test_register_user_duplicate_email(client):
    UserAccount.objects.create_user(email="duplikat@example.com", login="uzytkownik123", password="haslo123")
    payload = {
        "email": "duplikat@example.com",
        "login": "innylogin",
        "password": "haslo123"
    }
    response = client.post('/api/register/', payload, format='json')
    assert response.status_code == 400

# Test: poprawne logowanie użytkownika — powinien zwrócić tokeny JWT
@pytest.mark.django_db
def test_login_user_success(client):
    user = UserAccount.objects.create_user(email="login@example.com", login="login123", password="haslo123")
    response = client.post('/api/login/', {
        "email": "login@example.com",
        "password": "haslo123"
    }, format='json')
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

# Test: nieprawidłowe dane logowania — powinien zwrócić 401
@pytest.mark.django_db
def test_login_user_wrong_credentials(client):
    response = client.post('/api/login/', {
        "email": "nie_istnieje@example.com",
        "password": "zle_haslo"
    }, format='json')
    assert response.status_code == 401

# Test: brakujące dane przy logowaniu — powinien zwrócić 400
@pytest.mark.django_db
def test_login_user_missing_fields(client):
    response = client.post('/api/login/', {"email": "bez_hasla@example.com"}, format='json')
    assert response.status_code == 400

# Test: pobieranie wszystkich ról użytkowników — powinien zwrócić 200 i listę
@pytest.mark.django_db
def test_get_roles(auth_client):
    Role.objects.create(rola="Admin")
    Role.objects.create(rola="Gracz")
    response = auth_client.get('/api/roles/')
    assert response.status_code == 200
    assert isinstance(response.data, list)

# Test: poprawne pobranie danych zalogowanego użytkownika
@pytest.mark.django_db
def test_get_settings_success(auth_client):
    response = auth_client.get('/api/settings')
    assert response.status_code == 200
    assert 'user' in response.data
    assert 'login' in response.data['user']
    assert 'email' in response.data['user']

# Test: poprawna aktualizacja danych użytkownika
@pytest.mark.django_db
def test_update_account_success(auth_client):
    payload = {
        "login": "nowylogin",
        "email": "nowyemail@example.com"
    }
    response = auth_client.post('/api/updateAccount', payload, format='json')
    assert response.status_code == 200
    assert response.data['user']['login'] == "nowylogin"
    assert response.data['user']['email'] == "nowyemail@example.com"

# Test: aktualizacja konta — zbyt krótki login
@pytest.mark.django_db
def test_update_account_invalid_login(auth_client):
    payload = {
        "login": "ab",
        "email": "valid@example.com"
    }
    response = auth_client.post('/api/updateAccount', payload, format='json')
    assert response.status_code == 400
    assert "Login musi mieć co najmniej 4 znaki!" in response.data.get('error', '')

# Test: aktualizacja konta — nieprawidłowy email
@pytest.mark.django_db
def test_update_account_invalid_email(auth_client):
    payload = {
        "login": "poprawnylogin",
        "email": "zlyemail"
    }
    response = auth_client.post('/api/updateAccount', payload, format='json')
    assert response.status_code == 400
    assert "Niepoprawny adres e-mail!" in response.data.get('error', '')

# Test: aktualizacja konta — email już zajęty
@pytest.mark.django_db
def test_update_account_duplicate_email(auth_client):
    UserAccount.objects.create_user(email="duplikat@example.com", login="inne", password="haslo123")
    payload = {
        "login": "nowylogin",
        "email": "duplikat@example.com"
    }
    response = auth_client.post('/api/updateAccount', payload, format='json')
    assert response.status_code == 400
    assert "Ten E-mail jest już zajęty." in response.data.get('error', '')

# Test: aktualizacja konta — login już zajęty
@pytest.mark.django_db
def test_update_account_duplicate_login(auth_client):
    UserAccount.objects.create_user(email="inny@example.com", login="duplikat", password="haslo123")
    payload = {
        "login": "duplikat",
        "email": "nowy@example.com"
    }
    response = auth_client.post('/api/updateAccount', payload, format='json')
    assert response.status_code == 400
    assert "Login jest już zajęty." in response.data.get('error', '')

# Test: poprawne usunięcie konta
@pytest.mark.django_db
def test_delete_account_success(auth_client):
    response = auth_client.post('/api/deleteAccount', format='json')
    assert response.status_code == 200
    assert response.data['success'] is True
    assert UserAccount.objects.count() == 0  # użytkownik powinien zostać usunięty

@pytest.mark.django_db
def test_user_profile_success(auth_client):
    user = UserAccount.objects.get(email="testuser@example.com")

    # Dodajemy zgadywania poprawne dla punktów z wymaganym polem guess_date
    UserGuessLog.objects.create(user=user, guessed_correctly=True, guess_date=date.today())
    UserGuessLogTransfer.objects.create(user=user, guessed_correctly=True, guess_date=date.today())

    response = auth_client.get('/api/profile/')
    assert response.status_code == 200
    assert response.data["login"] == user.login
    assert response.data["email"] == user.email
    assert response.data["points_guess"] == 100
    assert response.data["points_transfer"] == 100
    assert response.data["total_points"] == 200
    assert response.data["profile_picture"] is None

# Test: poprawne przesłanie zdjęcia profilowego
@pytest.mark.django_db
def test_upload_profile_picture_success(auth_client):
    image_content = b'testimagecontent'
    image_file = SimpleUploadedFile("test.jpg", image_content, content_type="image/jpeg")

    response = auth_client.post('/api/profile/upload-picture/', {'image': image_file}, format='multipart')
    assert response.status_code == 200
    assert response.data["success"] == "Zdjęcie profilowe zostało zapisane."

    user = UserAccount.objects.get(email="testuser@example.com")
    assert bytes(user.profile_picture) == image_content

# Test: próba przesłania bez pliku — powinno zwrócić 400
@pytest.mark.django_db
def test_upload_profile_picture_missing_file(auth_client):
    response = auth_client.post('/api/profile/upload-picture/', {}, format='multipart')
    assert response.status_code == 400
    assert "error" in response.data
    assert response.data["error"] == "Brak pliku w żądaniu!"

@pytest.mark.django_db
def test_start_transfer_game(auth_client, transfer_question):
    response = auth_client.get('/api/transfer/start')
    assert response.status_code == 200
    data = response.data
    # Sprawdzam że jest klucz transfer_details
    assert "transfer_details" in data
    transfer_details = data["transfer_details"]
    assert "from_club" in transfer_details
    assert "to_club" in transfer_details
    assert "transfer_amount" in transfer_details
    assert "remaining_attempts" in data
    assert "game_over" in data
    assert "guessed_correctly" in data
    # correct_player może być None lub stringiem
    assert "correct_player" in data

@pytest.mark.django_db
def test_guess_transfer_player_correct(auth_client, transfer_question):
    start_response = auth_client.get('/api/transfer/start')
    assert start_response.status_code == 200

    # Pobieramy nazwisko piłkarza z transferu
    correct_player_name = None
    
    today = date.today()
    question = TransferQuestionOfTheDay.objects.get(question_date=today)
    correct_player_name = question.transfer.player.name

    payload = {
        "player_name": correct_player_name
    }

    response = auth_client.post('/api/transfer/guess', payload, format='json')
    assert response.status_code == 200
    data = response.data
    assert data["guessed_correctly"] is True
    assert data["game_over"] is True
    assert data["correct_player"] == correct_player_name
    assert "remaining_attempts" in data
    assert "from_club" in data
    assert "to_club" in data
    assert "transfer_amount" in data

@pytest.mark.django_db
def test_guess_transfer_player_incorrect(auth_client, transfer_question):
    start_response = auth_client.get('/api/transfer/start')
    assert start_response.status_code == 200

    
    # Tworzymy zawodnika z unikalnym nazwiskiem, na pewno niepoprawnym
    wrong_player_name = "Niepoprawny Zawodnik XYZ"

    # Upewniamy się, że taki zawodnik nie istnieje
    assert not Player.objects.filter(name__iexact=wrong_player_name).exists()

    payload = {
        "player_name": wrong_player_name
    }

    response = auth_client.post('/api/transfer/guess', payload, format='json')
    assert response.status_code == 200
    data = response.data
    assert data["guessed_correctly"] is False
    assert "remaining_attempts" in data
    assert data["remaining_attempts"] >= 0
    # correct_player będzie None dopóki gra się nie zakończy
    assert data.get("correct_player") is None or isinstance(data.get("correct_player"), str)

@pytest.mark.django_db
def test_check_guess_missing_player_name(auth_client):
    url = reverse('check_guess')
    response = auth_client.post(url, data={})
    assert response.status_code == 400
    assert 'Brak nazwy piłkarza!' in response.data.get('error', '')

@pytest.mark.django_db
def test_check_guess_player_not_found_and_attempts_increment(user_auth_client, user, assign_target_player):
    log, created = UserGuessLog.objects.get_or_create(user=user, guess_date=date.today(), defaults={'guess_number': 0})
    guess_number_before = log.guess_number

    url = reverse('check_guess')
    response = user_auth_client.post(url, data={'player_name': 'Nonexistent Player'})

    assert response.status_code == 404

    error_message = response.data.get('error', '')
    assert ('Nie znaleziono piłkarza' in error_message or 'Skończyły Ci się próby' in error_message)

    log.refresh_from_db()
    assert log.guess_number == guess_number_before + 1



@pytest.mark.django_db
def test_check_guess_no_more_attempts_exception(user_auth_client, user, assign_target_player, target_player):
    url = reverse('check_guess')
    UserGuessLog.objects.create(user=user, guess_date=date.today(), guess_number=5)

    response = user_auth_client.post(url, data={'player_name': target_player.name})

    assert response.status_code == 403

    error_message = response.data.get('error', '')
    assert 'Brak prób. Piłkarz to:' in error_message
    assert target_player.name in error_message

@pytest.mark.django_db
def test_check_guess_already_guessed_exception(user_auth_client, user, assign_target_player, target_player):
    url = reverse('check_guess')
    UserGuessLog.objects.create(user=user, guess_date=date.today(), guessed_correctly=True)

    response = user_auth_client.post(url, data={'player_name': target_player.name})

    assert response.status_code == 403

    error_message = response.data.get('error', '')
    assert 'Już zgadłeś.' in error_message
    assert target_player.name in error_message

@pytest.mark.django_db
def test_check_guess_correct_guess(user_auth_client, user, assign_target_player, target_player):
    url = reverse('check_guess')
    response = user_auth_client.post(url, data={'player_name': target_player.name})
    assert response.status_code == 200
    assert response.data.get('correct') is True
    assert response.data.get('remaining_attempts') == 4
    assert response.data.get('player_data', {}).get('name') == target_player.name
    assert response.data.get('game_over') is True

    log = UserGuessLog.objects.filter(user=user, guess_date=date.today()).first()
    assert log is not None
    assert log.guessed_correctly is True



@pytest.mark.django_db
def test_check_guess_incorrect_guess_with_remaining_attempts(user_auth_client, user, assign_target_player, guessed_player, target_player):
    assert assign_target_player.user == user
    assert assign_target_player.player == target_player

    assert guessed_player.name != target_player.name
    assert guessed_player.pk != target_player.pk

    # Tworzymy nowy obiekt Age o innej wartości niż target_player.age
    new_age = Age.objects.create(value=target_player.age.value + 1)
    guessed_player.age = new_age
    guessed_player.save()

    UserGuessLog.objects.filter(user=user, guess_date=date.today()).delete()
    UserGuessLog.objects.create(user=user, guess_date=date.today(), guess_number=0, guessed_correctly=False)

    start_url = reverse('get_game_status')
    start_response = user_auth_client.get(start_url)
    assert start_response.status_code == 200

    check_guess_url = reverse('check_guess')
    response = user_auth_client.post(check_guess_url, data={'player_name': guessed_player.name})
    assert response.status_code == 200
    data = response.data

    assert data.get('correct') is False
    assert data.get('remaining_attempts') == 4
    assert data.get('game_over') is False
    
    player_data = data.get('player_data', {})
    assert player_data.get('name') == guessed_player.name
    assert 'matches' in data

@pytest.mark.django_db
def test_get_user_detail_as_admin(auth_client, user):
    url = f'/api/users/{user.id}/'
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == user.id
    assert response.data['email'] == user.email
    assert response.data['login'] == user.login


@pytest.mark.django_db
def test_get_user_detail_not_found(auth_client):
    url = f'/api/users/9999/' 
    response = auth_client.get(url)

    assert response.status_code == 404
    assert 'error' in response.data


@pytest.mark.django_db
def test_delete_user_as_admin(auth_client, user):
    url = f'/api/users/{user.id}/'
    response = auth_client.delete(url)

    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['message'] == 'Użytkownik został usunięty.'

    assert not UserAccount.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_delete_user_not_found(auth_client):
    url = f'/api/users/9999/'
    response = auth_client.delete(url)

    assert response.status_code == 404
    assert 'error' in response.data


@pytest.mark.django_db
def test_user_detail_non_admin_forbidden(user_auth_client, user):
    url = f'/api/users/{user.id}/'

    response = user_auth_client.get(url)
    assert response.status_code == 403

    response = user_auth_client.delete(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_player_names_with_query(auth_client, player_data):
    # Dodajemy piłkarza do bazy
    Player.objects.create(
        name="Lewandowski",
        **player_data
    )
    Player.objects.create(
        name="Messi",
        **player_data
    )

    url = reverse('get_player_names')
    response = auth_client.get(url, {'query': 'Le'})

    assert response.status_code == 200
    assert 'players' in response.data
    player_names = response.data['players']
    assert isinstance(player_names, list)
    assert "Lewandowski" in player_names
    assert "Messi" not in player_names  # bo nie pasuje do "Le"

@pytest.mark.django_db
def test_get_player_names_without_query(auth_client, player_data):
    # Dodajemy kilku piłkarzy
    Player.objects.create(name="Zidane", **player_data)
    Player.objects.create(name="Ronaldo", **player_data)
    Player.objects.create(name="Benzema", **player_data)

    url = reverse('get_player_names')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert 'players' in response.data
    assert isinstance(response.data['players'], list)
    assert len(response.data['players']) <= 10