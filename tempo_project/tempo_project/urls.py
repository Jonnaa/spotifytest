"""
URL configuration for tempo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from tempo_app import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    # This is just so the app goes somewhere when it's first opened
    # We can change or modify in any way
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    # changed int to str to match Spotify data type 
    path('artist/<str:artist_name>/', views.artist, name='artist'),
    path('artist_api/', views.artist_api, name='artist_api'),
    path('seed_artists/',views.seed_artists, name='seed_artists'),
    path('player/<str:track_id>/', views.player, name='player'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('merch/', views.merch, name='merch'),
    path('merch/<int:merch_id>/', views.merch_detail, name='merch_details'),
    path('merch/create/', views.MerchCreate.as_view(), name='merch_create'),
    path('merch/<int:pk>/update/', views.MerchUpdate.as_view(), name='merch_update'),
    path('merch/<int:pk>/delete/', views.MerchDelete.as_view(), name='merch_delete'),

    # path('refresh_token/', views.refresh_token, name='refresh_token'),
]