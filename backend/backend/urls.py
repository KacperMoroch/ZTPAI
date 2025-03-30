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
from api.views import ExampleView, get_roles, get_user, get_all_users, get_player, get_all_players, login_user, register_user
from rest_framework_simplejwt.views import TokenObtainPairView


# lista tras URL które będą obsługiwane przez Django
urlpatterns = [
    # ścieżka do panelu administracyjnego Django
    path('admin/', admin.site.urls),

    # ścieżka do przykładowego widoku APIView, widoku opartego na klasie
    path('api/example/', ExampleView.as_view(), name='example'),

    # ścieżka do pobrania listy wszystkich użytkowników
    path('api/users/', get_all_users, name='get_all_users'),

    # scieżka do pobrania konkretnego użytkownika po ID
    path('api/users/<int:id>/', get_user, name='get_user'),

    # ścieżka do pobrania listy wszystkich piłkarzy
    path('api/players/', get_all_players, name='get_all_players'),

    # ścieżka do pobrania konkretnego piłkarza po ID
    path('api/players/<int:id>/', get_player, name='get_player'),

    # ścieżka do pobrania listy ról użytkowników
    path('api/roles/', get_roles, name='get_roles'), 

    # Ścieżka do rejestracji nowego użytkownika
    path('api/register/', register_user, name='register_user'),

    # ścieżka do logowania użytkownika za pomocą JWT
    path('api/login/', TokenObtainPairView.as_view(), name='login_user'),
]


