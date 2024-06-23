from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('join_request/', views.join_request, name='join_request'),
    path('my_club/', views.my_club, name='my_club')
]
