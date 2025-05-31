from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
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
    user = request.user
    return Response({
        'user': {
            'login': user.login,
            'email': user.email
        }
    })



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
    login = data.get('login')
    email = data.get('email')

    if not login or len(login) < 4:
        raise InvalidLoginException()

    if not email or '@' not in email:
        raise InvalidEmailException()

    user = request.user
    user.login = login
    user.email = email

    try:
        user.full_clean()
        user.save()
    except ValidationError as e:
        for field, messages in e.message_dict.items():
            for msg in messages:
                if 'email' in field and 'already exists' in msg.lower():
                    raise EmailTakenException()
                elif 'login' in field and 'already exists' in msg.lower():
                    raise LoginTakenException()
        raise AccountUpdateFailedException(detail=' '.join([msg for m in e.message_dict.values() for msg in m]))

    except IntegrityError:
        raise AccountUpdateFailedException(detail="Podany e-mail lub login jest już zajęty!")

    except Exception as e:
        raise AccountUpdateFailedException(detail=f'Wystąpił błąd: {str(e)}')

    return Response({
        'success': 'Dane zostały pomyślnie zaktualizowane!',
        'user': {
            'login': user.login,
            'email': user.email
        }
    })




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
    user = request.user
    user.delete()
    return Response({'success': True})
