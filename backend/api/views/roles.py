from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Role



@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę dostępnych ról",
    responses={
        200: openapi.Response(description="Lista ról")
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_roles(request):
    roles = Role.objects.all()
    role_list = [{"id": role.id, "rola": role.rola} for role in roles]
    return Response(role_list, status=status.HTTP_200_OK)
