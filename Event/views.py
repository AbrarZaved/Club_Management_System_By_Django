from django.shortcuts import redirect, render

from Event.forms import EventForm
from Event.models import Event, EventAttender
from Member.models import MemberJoined
from authentication.models import Student


# Create your views here.
def event(request):
    user = request.user
    student = Student.objects.get(user=user)
    clubs = list(
        MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )
    )

    events = Event.objects.filter(event_club__club_name__in=clubs)

    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "event/event.html")
    return render(request, "event/event.html", {"form": form, "events": events})


def event_attendee(request, boom):
    event = Event.objects.get(id=boom)
    student = Student.objects.get(user=request.user)
    EventAttender.objects.create(event=event, student=student, is_going=True)
    return redirect('event')
