from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserAccount

# Importy własnych wyjątków
from api.exceptions import (
    MissingFieldsException, EmailExistsException, LoginExistsException,
    RegistrationFailedException, InvalidCredentialsException, LoginFailedException,
    NoUsersFoundException, UserNotFoundException
)
from ..tasks import send_registration_email


def get_all_users_service():
    users = UserAccount.objects.all()   # Pobranie wszystkich użytkowników
    if not users.exists():
        raise NoUsersFoundException()   # Brak użytkowników to  wyjątek
    return users


def get_user_by_id_service(user_id):
    user = UserAccount.objects.filter(pk=user_id).first()  # Szukamy użytkownika po ID
    if not user:
        raise UserNotFoundException()  # Jeśli nie znaleziono, rzucamy wyjątek
    return user


def register_user_service(email, login, password):
    # Walidacja: sprawdzamy, czy wszystkie pola są obecne
    if not email or not login or not password:
        raise MissingFieldsException()

    # Sprawdzamy, czy email lub login są już zajęte 
    if UserAccount.objects.filter(email=email).exists():
        raise EmailExistsException()
    if UserAccount.objects.filter(login=login).exists():
        raise LoginExistsException()


    try:
        user = UserAccount.objects.create_user(email=email, login=login, password=password)
    except Exception:
        raise RegistrationFailedException()

    # Zadanie mailowe
    try:
        send_registration_email.delay(email)
    except Exception as e:
        print(f"Błąd Celery: {e}")

    # JWT token
    refresh = RefreshToken.for_user(user)
    return {
        "message": "Użytkownik zarejestrowany pomyślnie!",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def login_user_service(email, password, request=None):
    # Walidacja pól
    if not email or not password:
        raise MissingFieldsException()

    # Próba uwierzytelnienia użytkownika
    user = authenticate(request=request, email=email, password=password)

    # Jeśli uwierzytelnienie się nie powiedzie
    if user is None:
        raise InvalidCredentialsException()

    try:
        # Generowanie tokenów JWT
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_superuser": str(user.is_superuser),
            "message": "Zalogowano pomyślnie!"
        }
    except Exception:
        raise LoginFailedException()
