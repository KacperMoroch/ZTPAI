from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.serializers import UserAccountSerializer
from ..models import UserAccount
from ..exceptions import UserNotFoundException
from api.permissions import IsAdminUserCustom


user_id_param = openapi.Parameter(
    'id',
    openapi.IN_PATH,
    description="ID użytkownika",
    type=openapi.TYPE_INTEGER
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[user_id_param],
    operation_description="Pobierz dane użytkownika na podstawie jego ID.",
    responses={
        200: UserAccountSerializer,
        404: openapi.Response(description="Użytkownik nie został znaleziony.")
    }
)
@swagger_auto_schema(
    method='delete',
    manual_parameters=[user_id_param],
    operation_description="Usuń użytkownika na podstawie jego ID.",
    responses={
        200: openapi.Response(description="Użytkownik został usunięty."),
        404: openapi.Response(description="Użytkownik nie został znaleziony.")
    }
)
@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def user_detail(request, id):
    try:
        user = UserAccount.objects.get(pk=id)
    except UserAccount.DoesNotExist:
        raise UserNotFoundException()

    if request.method == 'GET':
        serializer = UserAccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response({
            'success': True,
            'message': 'Użytkownik został usunięty.'
        }, status=status.HTTP_200_OK)
