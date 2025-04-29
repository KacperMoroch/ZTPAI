from rest_framework.exceptions import APIException

class MissingFieldsException(APIException):
    status_code = 400
    default_detail = "Wszystkie pola są wymagane!"
    default_code = "missing_fields"

class EmailExistsException(APIException):
    status_code = 400
    default_detail = "Użytkownik o podanym e-mailu już istnieje!"
    default_code = "email_exists"

class LoginExistsException(APIException):
    status_code = 400
    default_detail = "Login jest już zajęty!"
    default_code = "login_exists"

class RegistrationFailedException(APIException):
    status_code = 500
    default_detail = "Błąd rejestracji użytkownika!"
    default_code = "registration_failed"

class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Nieprawidłowe dane logowania!"
    default_code = "invalid_credentials"

class LoginFailedException(APIException):
    status_code = 500
    default_detail = "Błąd logowania!"
    default_code = "login_failed"

class NoUsersFoundException(APIException):
    status_code = 204
    default_detail = "Brak użytkowników w bazie danych!"
    default_code = "no_users_found"

class NoPlayersFoundException(APIException):
    status_code = 204
    default_detail = "Brak piłkarzy w bazie danych!"
    default_code = "no_players_found"

class PlayerNotFoundException(APIException):
    status_code = 404
    default_detail = "Piłkarz nie został znaleziony!"
    default_code = "player_not_found"

class UserNotFoundException(APIException):
    status_code = 404
    default_detail = "Użytkownik nie został znaleziony!"
    default_code = "user_not_found"