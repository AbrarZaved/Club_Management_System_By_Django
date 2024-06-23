from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('demo/', views.demo, name='demo'),
    path('test/', lambda request: HttpResponse("Test URL is working"), name='test'),
]
