"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path # import funkcji `path` do definiowania tras URL

from api.views.guess_transfer import guess_transfer_player, start_transfer_game
from api.views.admin_panel import user_detail
from api.views.profile import upload_profile_picture, user_profile  

from api.views.settings import delete_account, get_settings, update_account
from api.views.guess_player import check_guess, get_player_names, get_game_status


from api.views.users import get_all_users, get_user, register_user, login_user 
from api.views.players import get_all_players, get_player
from api.views.roles import get_roles
from api.views.example import ExampleView

# from api.views import ExampleView, get_roles, get_user, get_all_users, get_player, get_all_players, login_user, register_user


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# lista tras URL które będą obsługiwane przez Django
urlpatterns = [
    # ścieżka do panelu administracyjnego Django
    path('admin/', admin.site.urls),

    # ścieżka do przykładowego widoku APIView, widoku opartego na klasie
    path('api/example/', ExampleView.as_view(), name='example'),

    # ścieżka do pobrania listy wszystkich użytkowników
    path('api/users/', get_all_users, name='get_all_users'),

    # # scieżka do pobrania konkretnego użytkownika po ID
    # path('api/users/<int:id>/', get_user, name='get_user'),

    # ścieżka do pobrania listy wszystkich piłkarzy
    path('api/players/', get_all_players, name='get_all_players'),

    # ścieżka do pobrania konkretnego piłkarza po ID
    path('api/players/<int:id>/', get_player, name='get_player'),

    # ścieżka do pobrania listy ról użytkowników
    path('api/roles/', get_roles, name='get_roles'), 

    # Ścieżka do rejestracji nowego użytkownika
    path('api/register/', register_user, name='register_user'),

    # ścieżka do logowania użytkownika za pomocą JWT
    path('api/login/', login_user, name='login_user'),

    # endpoint do odświeżenia tokenu JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/guess/', check_guess, name='check_guess'),
    path('api/player-names/', get_player_names,name='get_player_names'),
    path('api/game-status/', get_game_status, name='get_game_status'),


    path('api/settings', get_settings, name='get_settings'),
    path('api/updateAccount', update_account, name='update_account'),
    path('api/deleteAccount', delete_account, name='delete_account'),

    path('api/profile/', user_profile, name='user_profile'),

    path('api/users/<int:id>/', user_detail, name='user_detail'),

    path('api/transfer/start', start_transfer_game, name='start_transfer_game'),
    path('api/transfer/guess', guess_transfer_player, name='guess_transfer_player'),

    path('api/profile/upload-picture/', upload_profile_picture,name='upload_profile_picture'),

]

# Konfiguracja dokumentacji Swagger / ReDoc
schema_view = get_schema_view(
   openapi.Info(
      title="Goaldle API",  # Nazwa API
      default_version='v1',
      description="Dokumentacja API dla Goaldle",
      terms_of_service="https://www.example.com/terms/",  # Link do regulaminu
      contact=openapi.Contact(email="kontakt@example.com"),  # Kontakt do autora
      license=openapi.License(name="MIT License"),  # Informacja o licencji
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # Dokumentacja dostępna publicznie
)

# Dodanie ścieżek do interfejsów dokumentacji API
urlpatterns += [
    # Swagger UI (graficzna dokumentacja API)
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ReDoc UI (alternatywna dokumentacja)
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Surowy plik JSON z opisem API (do integracji lub eksportu)
    path('api/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]