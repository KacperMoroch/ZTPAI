from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.serializers import UserAccountSerializer
from api.permissions import IsAdminUserCustom
from api.services.user_service import (
    get_all_users_service,
    get_user_by_id_service,
    register_user_service,
    login_user_service
)


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę wszystkich użytkowników",
    responses={
        200: openapi.Response(
            description="Lista użytkowników",
            schema=UserAccountSerializer(many=True)
        ),
        204: "Brak użytkowników",
        500: "Błąd serwera"
    }
)
@authentication_classes([JWTAuthentication])  # Uwierzytelnianie JWT
@permission_classes([IsAuthenticated, IsAdminUserCustom])  # Tylko zalogowani admini mają dostęp
@api_view(['GET'])
def get_all_users(request):
    users = get_all_users_service()
    serializer = UserAccountSerializer(users, many=True)  # Serializacja listy użytkowników
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz dane użytkownika po ID",
    responses={
        200: openapi.Response(
            description="Dane użytkownika",
            schema=UserAccountSerializer()
        ),
        404: "Użytkownik nie znaleziony"
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
@api_view(['GET'])
def get_user(request, id):
    user = get_user_by_id_service(id)
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
        201: openapi.Response(
            description="Użytkownik zarejestrowany",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                }
            )
        ),
        400: openapi.Response(description="Błąd walidacji"),
        500: openapi.Response(description="Błąd serwera")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Dostępne bez logowania
def register_user(request):
    # Pobieramy dane z requestu
    email = request.data.get('email')
    login = request.data.get('login')
    password = request.data.get('password')

    response_data = register_user_service(email, login, password)
    return Response(response_data, status=status.HTTP_201_CREATED)


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
        200: openapi.Response(
            description="Zalogowano pomyślnie",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                    'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Czy użytkownik ma uprawnienia administratora')
                }
            )
        ),
        400: openapi.Response(description="Brak wymaganych danych"),
        401: openapi.Response(description="Nieprawidłowe dane logowania")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    # Pobranie danych logowania z requestu
    email = request.data.get('email')
    password = request.data.get('password')

    response_data = login_user_service(email, password, request)
    return Response(response_data, status=status.HTTP_200_OK)
