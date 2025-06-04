from ..models import UserAccount
from ..exceptions import UserNotFoundException

def get_user_by_id(user_id: int) -> UserAccount:
    try:
        return UserAccount.objects.get(pk=user_id)
    except UserAccount.DoesNotExist:
        raise UserNotFoundException()

def delete_user_by_id(user_id: int) -> None:
    user = get_user_by_id(user_id)
    user.delete()
