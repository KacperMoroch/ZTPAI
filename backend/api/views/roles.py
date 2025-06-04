from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import RoleSerializer
from ..services.role_service import get_all_roles


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę dostępnych ról. Wynikiem jest lista obiektów zawierających identyfikator oraz nazwę roli.",
    responses={200: openapi.Response(
        description="Lista ról",
        schema=RoleSerializer(many=True)
    )}
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_roles(request):
    roles_data = get_all_roles()
    return Response(roles_data, status=status.HTTP_200_OK)
