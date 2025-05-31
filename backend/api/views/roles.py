from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from api.models import Role
from api.serializers import RoleSerializer
from drf_yasg import openapi

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
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
