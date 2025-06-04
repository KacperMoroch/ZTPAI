import base64
from api.models import UserGuessLog, UserGuessLogTransfer
from api.exceptions import MissingFileException


def get_user_profile(user):
    correct_guesses = UserGuessLog.objects.filter(user=user, guessed_correctly=True).count()
    points_guess = correct_guesses * 100

    correct_guesses_transfer = UserGuessLogTransfer.objects.filter(user=user, guessed_correctly=True).count()
    points_guess_transfer = correct_guesses_transfer * 100

    total = points_guess + points_guess_transfer

    profile_picture_base64 = None
    if user.profile_picture:
        profile_picture_base64 = base64.b64encode(user.profile_picture).decode('utf-8')

    return {
        "login": user.login,
        "email": user.email,
        "created_at": user.created_at,
        "points_guess": points_guess,
        "points_transfer": points_guess_transfer,
        "total_points": total,
        "profile_picture": profile_picture_base64,
    }


def save_profile_picture(user, image_file):
    if not image_file:
        raise MissingFileException()

    # zapisujemy obrazek binarnie w polu modelu user.profile_picture (pole typu BinaryField)
    user.profile_picture = image_file.read()
    user.save()
    return {"success": "Zdjęcie profilowe zostało zapisane."}
