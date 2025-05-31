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

class InvalidLoginException(APIException):
    status_code = 400
    default_detail = "Login musi mieć co najmniej 4 znaki!"
    default_code = "invalid_login"

class InvalidEmailException(APIException):
    status_code = 400
    default_detail = "Niepoprawny adres e-mail!"
    default_code = "invalid_email"

class EmailTakenException(APIException):
    status_code = 400
    default_detail = "Ten E-mail jest już zajęty."
    default_code = "email_taken"

class LoginTakenException(APIException):
    status_code = 400
    default_detail = "Login jest już zajęty."
    default_code = "login_taken"

class AccountUpdateFailedException(APIException):
    status_code = 500
    default_detail = "Wystąpił błąd podczas aktualizacji konta!"
    default_code = "account_update_failed"

class MissingFileException(APIException):
    status_code = 400
    default_detail = "Brak pliku w żądaniu!"
    default_code = "missing_file"

class MissingPlayerNameException(APIException):
    status_code = 400
    default_detail = "Brak nazwy piłkarza!"
    default_code = "missing_player_name"

class GameNotStartedException(APIException):
    status_code = 400
    default_detail = "Gra nie została jeszcze rozpoczęta."
    default_code = "game_not_started"

class NoMoreAttemptsException(APIException):
    status_code = 403
    default_detail = "Wykorzystano wszystkie próby. Spróbuj ponownie jutro."
    default_code = "no_more_attempts"
    
class AlreadyGuessedException(APIException):
    status_code = 403
    default_detail = "Już zgadłeś dzisiaj piłkarza."
    default_code = "already_guessed"