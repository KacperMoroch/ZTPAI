from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from ..services.user_profile_service import get_user_profile, save_profile_picture


@swagger_auto_schema(
    method='get',
    operation_description="Zwraca profil zalogowanego użytkownika, w tym login, email, datę utworzenia konta, liczbę punktów za zgadywanie oraz zdjęcie profilowe (jeśli istnieje) zakodowane w base64.",
    responses={
        200: openapi.Response(
            description="Dane profilu użytkownika",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "login": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                    "points_guess": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "points_transfer": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "total_points": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "profile_picture": openapi.Schema(type=openapi.TYPE_STRING, description="Base64 lub null", nullable=True),
                }
            )
        ),
        401: openapi.Response(description="Brak autoryzacji")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response(get_user_profile(request.user))


@swagger_auto_schema(
    method='post',
    operation_description="Prześlij zdjęcie profilowe użytkownika (multipart/form-data). Pole `image` jest wymagane.",
    manual_parameters=[
        openapi.Parameter(
            name="image",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Plik obrazu (zdjęcie profilowe)"
        )
    ],
    responses={
        200: openapi.Response(
            description="Zdjęcie zapisane",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: openapi.Response(
            description="Brak pliku w żądaniu",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        401: openapi.Response(description="Brak autoryzacji"),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_picture(request):
    image_file = request.FILES.get("image")
    result = save_profile_picture(request.user, image_file)
    return Response(result, status=status.HTTP_200_OK)
