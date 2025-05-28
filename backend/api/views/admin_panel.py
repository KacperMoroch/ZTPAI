from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response

from api.serializers import UserAccountSerializer
from ..models import UserAccount
from ..exceptions import UserNotFoundException
from api.permissions import IsAdminUserCustom


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
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'success': True, 'message': 'User deleted'}, status=status.HTTP_200_OK)
