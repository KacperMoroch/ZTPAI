from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ExampleView(APIView):

    @swagger_auto_schema(
        operation_description="Zwraca dane przykładowego użytkownika.",
        responses={
            200: openapi.Response(
                description="Dane użytkownika",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, example="Karol Kłos"),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, example="karol.klos@gmail.com"),
                    }
                )
            )
        }
    )
    def get(self, request):
        data = {
            "id": 1,
            "name": "Karol Kłos",
            "email": "karol.klos@gmail.com"
        }
        return Response(data, status=status.HTTP_200_OK)
