from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from ..models import Player
from ..serializers import PlayerSerializer
from ..exceptions import PlayerNotFoundException
from rest_framework.pagination import PageNumberPagination


class PlayerPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10


def fetch_all_players(request):
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


def fetch_player_by_id(player_id):
    player = Player.objects.filter(pk=player_id).first()
    if not player:
        raise PlayerNotFoundException()
    serializer = PlayerSerializer(player)
    return Response(serializer.data, status=status.HTTP_200_OK)


def fetch_unique_filters():
    countries = Player.objects.values_list('country__name', flat=True).distinct()
    leagues = Player.objects.values_list('league__name', flat=True).distinct()
    positions = Player.objects.values_list('position__name', flat=True).distinct()

    return Response({
        'countries': sorted(filter(None, countries)),
        'leagues': sorted(filter(None, leagues)),
        'positions': sorted(filter(None, positions)),
    })
