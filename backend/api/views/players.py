from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Player
from ..serializers import PlayerSerializer
from ..exceptions import NoPlayersFoundException, PlayerNotFoundException

from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

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
    query = Q()
    country = request.GET.get('country')
    league = request.GET.get('league')
    position = request.GET.get('position')

    if country:
        query &= Q(country__name__icontains=country)
    if league:
        query &= Q(league__name__icontains=league)
    if position:
        query &= Q(position__name__icontains=position)

    sort = request.GET.get('sort')
    valid_sorts = ['name', '-name', 'age__value', '-age__value']
    if sort not in valid_sorts:
        sort = 'name'

    players = Player.objects.filter(query).order_by(sort)

    paginator = PlayerPagination()
    page = paginator.paginate_queryset(players, request)

    # nawet jeśli page to None (czyli brak wyników), dalej zwracamy pustą listę
    serializer = PlayerSerializer(page or [], many=True)
    return paginator.get_paginated_response(serializer.data)


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
    player = Player.objects.filter(pk=id).first()
    if not player:
        raise PlayerNotFoundException()
    serializer = PlayerSerializer(player)
    return Response(serializer.data, status=status.HTTP_200_OK)




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
    countries = Player.objects.values_list('country__name', flat=True).distinct()
    leagues = Player.objects.values_list('league__name', flat=True).distinct()
    positions = Player.objects.values_list('position__name', flat=True).distinct()

    return Response({
        'countries': sorted(filter(None, countries)),
        'leagues': sorted(filter(None, leagues)),
        'positions': sorted(filter(None, positions)),
    })
