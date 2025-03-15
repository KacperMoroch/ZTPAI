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
from django.urls import path
from api.views import ExampleView, get_user, get_all_users, get_player, get_all_players


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/example/', ExampleView.as_view(), name='example'),
    path('api/users/', get_all_users, name='get_all_users'),
    path('api/users/<int:id>/', get_user, name='get_user'),
    path('api/players/', get_all_players, name='get_all_players'),
    path('api/players/<int:id>/', get_player, name='get_player'),
]
