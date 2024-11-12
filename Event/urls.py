from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

urlpatterns = [
    path("event", views.event, name="event"),
    path("event_attendee/<int:boom>", views.event_attendee, name="event_attendee"),
]
