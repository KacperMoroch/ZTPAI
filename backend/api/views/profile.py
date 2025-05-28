from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from api.models import UserGuessLog

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # Liczenie poprawnych zgadywań i mnożenie razy 100
    correct_guesses = UserGuessLog.objects.filter(user=user, guessed_correctly=True).count()
    points_guess = correct_guesses * 100

    # Liczenie punktów za transfery
    # points_transfer = UserGuessLogTransfer.objects.filter(user=user, guessed_correctly=True).count()


    # Tymczasowe punkty za transfery – 0
    points_transfer = 0

    total = points_guess + points_transfer

    profile_data = {
        "login": user.login,
        "email": user.email,
        "created_at": user.created_at,
        "points_guess": points_guess,
        "points_transfer": points_transfer,
        "total_points": total
    }

    return Response(profile_data)
