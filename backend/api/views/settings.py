from django.http import JsonResponse
from django.db import IntegrityError
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.core.exceptions import ValidationError

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

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_account(request):
    data = request.data
    login = data.get('login')
    email = data.get('email')

    if not login or len(login) < 4:
        return Response({'error': 'Login musi mieć co najmniej 4 znaki!'})

    if not email or '@' not in email:
        return Response({'error': 'Niepoprawny adres e-mail!'})

    user = request.user
    user.login = login
    user.email = email

    try:
        user.full_clean()
        user.save()
    except ValidationError as e:
        error_messages = []
        for field, messages in e.message_dict.items():
            for msg in messages:
                if 'email' in field and 'already exists' in msg.lower():
                    error_messages.append("Ten E-mail jest już zajęty.")
                elif 'login' in field and 'already exists' in msg.lower():
                    error_messages.append("Login jest już zajęty.")
                else:
                    error_messages.append(msg)
        return Response({'error': ' '.join(error_messages)})

    except IntegrityError:
        return Response({'error': 'Podany e-mail lub login jest już zajęty!'})

    except Exception as e:
        return Response({'error': f'Wystąpił błąd: {str(e)}'})

    return Response({
        'success': 'Dane zostały pomyślnie zaktualizowane!',
        'user': {
            'login': user.login,
            'email': user.email
        }
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return JsonResponse({'success': True})
