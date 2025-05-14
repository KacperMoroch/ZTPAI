from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..tasks import send_registration_email

# Importy własnych wyjątków
from api.exceptions import (MissingFieldsException, EmailExistsException, LoginExistsException,
                           RegistrationFailedException, InvalidCredentialsException, LoginFailedException,
                           NoUsersFoundException, UserNotFoundException)

from api.serializers import UserAccountSerializer
from api.models import UserAccount
from api.permissions import IsAdminUserCustom





@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę wszystkich użytkowników",
    responses={
        200: openapi.Response(description="Lista użytkowników"),
        204: "Brak użytkowników",
        500: "Błąd serwera"
    }
)
@authentication_classes([JWTAuthentication])  # Uwierzytelnianie JWT
@permission_classes([IsAuthenticated, IsAdminUserCustom])  # Tylko zalogowani admini mają dostęp
@api_view(['GET'])
def get_all_users(request):
    users = UserAccount.objects.all()  # Pobranie wszystkich użytkowników
    if not users.exists():
        raise NoUsersFoundException()  # Brak użytkowników to  wyjątek
    serializer = UserAccountSerializer(users, many=True)  # Serializacja listy użytkowników
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    operation_description="Pobierz dane użytkownika po ID",
    responses={
        200: openapi.Response(description="Dane użytkownika"),
        404: "Użytkownik nie znaleziony"
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
@api_view(['GET'])
def get_user(request, id):
    user = UserAccount.objects.filter(pk=id).first()  # Szukamy użytkownika po ID
    if not user:
        raise UserNotFoundException()  # Jeśli nie znaleziono, rzucamy wyjątek
    serializer = UserAccountSerializer(user)  # Serializujemy pojedynczego użytkownika
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='post',
    operation_description="Rejestracja nowego użytkownika",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'login', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Adres email'),
            'login': openapi.Schema(type=openapi.TYPE_STRING, description='Login użytkownika'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Hasło'),
        },
    ),
    responses={
        201: openapi.Response(description="Użytkownik zarejestrowany"),
        400: "Błąd walidacji",
        500: "Błąd serwera"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Dostępne bez logowania
def register_user(request):
    # Pobieramy dane z requestu
    email = request.data.get('email')
    login = request.data.get('login')
    password = request.data.get('password')

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

    return Response({
        "message": "Użytkownik zarejestrowany pomyślnie!",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }, status=status.HTTP_201_CREATED)




@swagger_auto_schema(
    method='post',
    operation_description="Logowanie użytkownika. Zwraca token JWT",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email użytkownika'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Hasło'),
        },
    ),
    responses={
        200: openapi.Response(description="Zalogowano pomyślnie"),
        400: "Brak wymaganych danych",
        401: "Nieprawidłowe dane logowania"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    # Pobranie danych logowania z requestu
    email = request.data.get('email')
    password = request.data.get('password')

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
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_superuser": str(user.is_superuser),
            "message": "Zalogowano pomyślnie!"
        }, status=status.HTTP_200_OK)
    except Exception:
        raise LoginFailedException()