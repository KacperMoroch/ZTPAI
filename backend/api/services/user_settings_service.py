from django.db import IntegrityError
from django.core.exceptions import ValidationError
from api.exceptions import (
    InvalidLoginException,
    InvalidEmailException,
    EmailTakenException,
    LoginTakenException,
    AccountUpdateFailedException
)


def get_user_settings(user):
    return {
        'user': {
            'login': user.login,
            'email': user.email
        }
    }


def update_user_account(user, login, email):
    if not login or len(login) < 4:
        raise InvalidLoginException()

    if not email or '@' not in email:
        raise InvalidEmailException()

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

    return {
        'success': 'Dane zostały pomyślnie zaktualizowane!',
        'user': {
            'login': user.login,
            'email': user.email
        }
    }


def delete_user_account(user):
    user.delete()
    return {'success': True}
