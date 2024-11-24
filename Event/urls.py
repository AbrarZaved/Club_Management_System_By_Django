from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

urlpatterns = [
    path("event", views.event, name="event"),
    path("eventDetails/<int:pk>", views.event, name="eventDetails"),
    path("event_attendee/<int:boom>", views.event_attendee, name="event_attendee"),
    path("event_management", views.event_management, name="event_management"),
    path(
        "delete_event_attendee/<str:attendee_id>/<str:event_name>",
        csrf_exempt(views.delete_event_attendee),
        name="delete_event_attendee",
    ),
    path(
        "event_properties", csrf_exempt(views.event_properties), name="event_properties"
    ),
    path(
        "event_search", csrf_exempt(views.event_search), name="event_search"
    ),
]
