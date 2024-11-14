from django.shortcuts import redirect, render
from django.contrib import messages

from Dashboard.models import Club
from Event.forms import EventForm
from Event.models import Event, EventAttender
from Member.models import MemberJoined, Notification
from authentication.models import Student


# Create your views here.
def event(request):
    admin_name = request.user.username[6:]
    user = request.user
    student = Student.objects.get(user=user)
    clubs = list(
        MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )
    )
    club_list = [
        (
            (club),
            (Event.objects.filter(event_club__club_name=club)).count(),
        )
        for club in clubs
    ]
    print(club_list)
    events = Event.objects.filter(event_club__club_name__in=clubs)

    form = EventForm()
    if admin_name:
        club_name = Club.objects.get(tag=admin_name)
        events = Event.objects.filter(event_club__club_name=club_name)
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(request, "event")
        return render(request, "event/event.html", {"form": form, "events": events})
    Notification.objects.filter(
        Student__username=str(user), notification_type="events"
    ).delete()

    return render(
        request,
        "event/event.html",
        {"form": form, "events": events, "club_list": club_list},
    )


def event_attendee(request, boom):
    event = Event.objects.get(id=boom)
    student = Student.objects.get(user=request.user)
    if EventAttender.objects.filter(event=event, student=student).exists():
        messages.warning(request, "You have already registered for this event")
        return redirect("event")
    EventAttender.objects.create(event=event, student=student, is_going=True)
    return redirect("event")
