from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

urlpatterns = [
    path("add_event", views.add_event, name="event"),
]
