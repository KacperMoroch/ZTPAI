from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..exceptions import (
    InvalidLoginException,
    InvalidEmailException,
    EmailTakenException,
    LoginTakenException,
    AccountUpdateFailedException
)
from ..services.user_settings_service import (
    get_user_settings,
    update_user_account,
    delete_user_account
)


@swagger_auto_schema(
    method='get',
    operation_description="Pobiera dane aktualnie zalogowanego użytkownika.",
    responses={
        200: openapi.Response(
            description="Dane użytkownika",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'login': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                }
            )
        ),
        401: openapi.Response(description="Brak autoryzacji")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_settings(request):
    data = get_user_settings(request.user)
    return Response(data)


@swagger_auto_schema(
    method='post',
    operation_description="Aktualizuje dane konta użytkownika (login i email).",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['login', 'email'],
        properties={
            'login': openapi.Schema(type=openapi.TYPE_STRING, description='Nowy login'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Nowy adres email'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Zaktualizowano dane",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'login': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                }
            )
        ),
        400: openapi.Response(description="Nieprawidłowe dane lub konflikt login/email"),
        500: openapi.Response(description="Błąd aktualizacji konta")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_account(request):
    data = request.data
    response_data = update_user_account(request.user, data.get('login'), data.get('email'))
    return Response(response_data)


@swagger_auto_schema(
    method='post',
    operation_description="Usuwa konto aktualnie zalogowanego użytkownika.",
    responses={
        200: openapi.Response(
            description="Konto zostało usunięte",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        ),
        401: openapi.Response(description="Brak autoryzacji")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    response_data = delete_user_account(request.user)
    return Response(response_data)
