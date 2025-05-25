import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import UserAccount, Player, Role

# Fixture inicjalizujący niezalogowanego klienta API
@pytest.fixture
def client():
    return APIClient()

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

# ======================= TESTY =======================

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

# Test: pobieranie listy graczy, gdy baza jest pusta — oczekiwany status 204 (brak danych)
@pytest.mark.django_db
def test_get_all_players_empty(auth_client):
    response = auth_client.get('/api/players/')
    assert response.status_code == 204

# Test: próba pobrania nieistniejącego gracza — oczekiwany status 404
@pytest.mark.django_db
def test_get_player_not_found(auth_client):
    response = auth_client.get('/api/players/999/')
    assert response.status_code == 404

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
