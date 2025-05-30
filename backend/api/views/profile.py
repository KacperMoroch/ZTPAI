from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from api.models import UserGuessLog, UserGuessLogTransfer
from rest_framework_simplejwt.authentication import JWTAuthentication
import base64


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # Liczenie poprawnych zgadywań i mnożenie razy 100
    correct_guesses = UserGuessLog.objects.filter(user=user, guessed_correctly=True).count()
    points_guess = correct_guesses * 100

    # Liczenie punktów za transfery
    correct_guesses_transfer = UserGuessLogTransfer.objects.filter(user=user, guessed_correctly=True).count()
    points_guess_transfer = correct_guesses_transfer * 100

    total = points_guess + points_guess_transfer

    # Zakodowanie zdjęcia profilowego do base64
    profile_picture_base64 = None
    if user.profile_picture:
        profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')

    profile_data = {
        "login": user.login,
        "email": user.email,
        "created_at": user.created_at,
        "points_guess": points_guess,
        "points_transfer": points_guess_transfer,
        "total_points": total,
        "profile_picture": profile_picture_base64,
    }

    return Response(profile_data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    file = request.FILES.get("image")
    if not file:
        return Response({"error": "Brak pliku."}, status=400)

    user = request.user
    user.profile_picture = file.read()
    user.save()

    return Response({"success": "Zdjęcie zapisane."})
