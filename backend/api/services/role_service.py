from api.models import Role
from api.serializers import RoleSerializer

def get_all_roles():
    roles = Role.objects.all()
    return RoleSerializer(roles, many=True).data
