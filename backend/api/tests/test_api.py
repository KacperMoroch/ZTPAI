import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import UserAccount, Player, Role

# Fixture do inicjalizacji klienta API dla testów
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def auth_client(client):
    user = UserAccount.objects.create_user(
        email="testuser@example.com",
        login="testuser",
        password="testpassword",
        is_superuser=True
    )
    response = client.post('/api/login/', {
        "email": "testuser@example.com",
        "password": "testpassword"
    }, format='json')

    assert response.status_code == 200, f"Login failed: {response.data}"
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client

# Testuje przykładowy endpoint, który powinien zwracać status 200 i dane z nazwiskiem Karola Kłosa
@pytest.mark.django_db
def test_example_view(auth_client):
    response = auth_client.get('/api/example/')
    assert response.status_code == 200
    assert response.data["name"] == "Karol Kłos"

# Testuje endpoint zwracający listę użytkowników, gdy brak użytkowników w bazie — oczekiwany status 200
@pytest.mark.django_db
def test_get_all_users_empty(auth_client):
    UserAccount.objects.exclude(email='testuser@example.com').delete()  
    response = auth_client.get('/api/users/')
    assert response.status_code == 200

# Testuje endpoint zwracający listę użytkowników, gdy użytkownik istnieje — oczekiwany status 200 i lista
@pytest.mark.django_db
def test_get_all_users_with_data(auth_client):
    #UserAccount.objects.all().delete()
    UserAccount.objects.create_user(email="test@example.com", login="innylogin", password="haslo123")
    response = auth_client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data, list)

# Testuje pobieranie konkretnego użytkownika po ID — oczekiwany status 200 i poprawne dane
@pytest.mark.django_db
def test_get_user_valid(auth_client):
    user = UserAccount.objects.create_user(email="jan@example.com", login="janek", password="haslo123")
    response = auth_client.get(f'/api/users/{user.id}/')
    assert response.status_code == 200
    assert response.data["email"] == "jan@example.com"

# Testuje próbę pobrania nieistniejącego użytkownika — oczekiwany status 404
@pytest.mark.django_db
def test_get_user_not_found(auth_client):
    response = auth_client.get('/api/users/999/')
    assert response.status_code == 404

# Testuje pobieranie listy graczy, gdy brak graczy w bazie — oczekiwany status 204
@pytest.mark.django_db
def test_get_all_players_empty(auth_client):
    response = auth_client.get('/api/players/')
    assert response.status_code == 204

# Testuje próbę pobrania nieistniejącego gracza — oczekiwany status 404
@pytest.mark.django_db
def test_get_player_not_found(auth_client):
    response = auth_client.get('/api/players/999/')
    assert response.status_code == 404

# Testuje poprawną rejestrację użytkownika — oczekiwany status 201
@pytest.mark.django_db
def test_register_user_success(client):
    payload = {
        "email": "nowy_uzytkownik@example.com",
        "login": "nowy_uzytkownik",
        "password": "haslo123"
    }
    response = client.post('/api/register/', payload, format='json')
    assert response.status_code == 201

# Testuje rejestrację z brakującymi polami — oczekiwany status 400
@pytest.mark.django_db
def test_register_user_missing_fields(client):
    response = client.post('/api/register/', {"email": "brak@example.com"}, format='json')
    assert response.status_code == 400

# Testuje rejestrację z istniejącym już adresem e-mail — oczekiwany status 400
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

# Testuje poprawne logowanie użytkownika — oczekiwany status 200 i otrzymanie tokenów JWT
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

# Testuje próbę logowania z niepoprawnymi danymi — oczekiwany status 401
@pytest.mark.django_db
def test_login_user_wrong_credentials(client):
    response = client.post('/api/login/', {
        "email": "nie_istnieje@example.com",
        "password": "zle_haslo"
    }, format='json')
    assert response.status_code == 401

# Testuje próbę logowania bez wymaganych pól — oczekiwany status 400
@pytest.mark.django_db
def test_login_user_missing_fields(client):
    response = client.post('/api/login/', {"email": "bez_hasla@example.com"}, format='json')
    assert response.status_code == 400

# Testuje pobieranie wszystkich ról — oczekiwany status 200 i lista ról
@pytest.mark.django_db
def test_get_roles(auth_client):
    Role.objects.create(rola="Admin")
    Role.objects.create(rola="Gracz")
    response = auth_client.get('/api/roles/')
    assert response.status_code == 200
    assert isinstance(response.data, list)
