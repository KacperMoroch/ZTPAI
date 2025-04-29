from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ExampleView(APIView):
    def get(self, request):
        data = {
            "id": 1,
            "name": "Karol Kłos",
            "email": "karol.klos@gmail.com"
        }
        return Response(data, status=status.HTTP_200_OK)
