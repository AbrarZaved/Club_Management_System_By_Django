from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('join_request/', views.join_request, name='join_request'),
    path('my_club/', views.my_club, name='my_club'),
    path('view_member/<int:boom>',views.view_member,name='view_member'),
    path('delete_member/<int:boom>',views.delete_member,name='delete_member')
]
