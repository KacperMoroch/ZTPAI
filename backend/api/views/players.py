from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers import PlayerSerializer
from ..exceptions import PlayerNotFoundException
from ..services.player_service import (
    fetch_all_players,
    fetch_player_by_id,
    fetch_unique_filters,
)

from rest_framework.pagination import PageNumberPagination


class PlayerPagination(PageNumberPagination):
    page_size = 3  # max 3 piłkarzy na stronę
    page_size_query_param = 'page_size'
    max_page_size = 10


player_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "country_name": openapi.Schema(type=openapi.TYPE_STRING),
        "league_name": openapi.Schema(type=openapi.TYPE_STRING),
        "club_name": openapi.Schema(type=openapi.TYPE_STRING),
        "position_name": openapi.Schema(type=openapi.TYPE_STRING),
        "age_value": openapi.Schema(type=openapi.TYPE_INTEGER),
        "shirt_number_value": openapi.Schema(type=openapi.TYPE_INTEGER),
    }
)


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz listę wszystkich piłkarzy.",
    responses={
        200: openapi.Response(
            description="Lista piłkarzy",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=player_schema
            )
        ),
        204: openapi.Response(
            description="Brak piłkarzy w bazie danych",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)}
            )
        ),
        401: openapi.Response(description="Brak autoryzacji"),
        500: openapi.Response(description="Błąd serwera")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_players(request):
    return fetch_all_players(request)


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz dane piłkarza po ID.",
    manual_parameters=[
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="ID piłkarza"
        )
    ],
    responses={
        200: openapi.Response(
            description="Dane piłkarza",
            schema=player_schema
        ),
        404: openapi.Response(
            description="Piłkarz nie został znaleziony",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)}
            )
        ),
        401: openapi.Response(description="Brak autoryzacji"),
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_player(request, id):
    return fetch_player_by_id(id)


@swagger_auto_schema(
    method='get',
    operation_description="Pobierz unikalne wartości filtrów (kraje, ligi, pozycje) dla piłkarzy.",
    responses={
        200: openapi.Response(
            description="Unikalne wartości filtrów",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'countries': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING)
                    ),
                    'leagues': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING)
                    ),
                    'positions': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING)
                    ),
                }
            )
        ),
        401: openapi.Response(description="Brak autoryzacji")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_unique_filters(request):
    return fetch_unique_filters()
