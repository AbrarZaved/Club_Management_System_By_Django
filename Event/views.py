from django.shortcuts import redirect, render
from django.contrib import messages

from Dashboard.models import Club
from Event.forms import EventForm
from Event.models import Event, EventAttender
from Member.models import MemberJoined, Notification
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
    if "admin" in request.user.username:
        admin_name = request.user.username[6:]
        club_name = Club.objects.get(tag=admin_name)
        events = Event.objects.filter(event_club__club_name=club_name)
        if request.method == "POST":
            form = EventForm(request.POST)
            if Event.objects.filter(event_name=form.event_name).exists():
                messages.warning(request, "Event already exists")
                return redirect("event")
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


def event_management(request):
    form = EventForm()
    admin_name = request.user.username[6:]
    club_name = Club.objects.get(tag=admin_name)
    members = MemberJoined.objects.filter(club=club_name)
    events = list(
        Event.objects.filter(event_club__club_name=club_name).values_list(
            "event_name", flat=True
        )
    )
    data = {}
    for event in events:
        attendees = EventAttender.objects.filter(event__event_name=event).values(
            "student__user__first_name",
            "student__user__last_name",
            "student__student_id",
            "student__user__email",
            "student__phone_number",
            "attended_at",
            "student__id",
            "student__profile_pic",
            "student__dept",
        )

        # Creating a list with full name and other details
        data[event] = [
            {
                "full_name": f"{attendee['student__user__first_name']} {attendee['student__user__last_name']}",
                "student_id": attendee["student__student_id"],
                "email": attendee["student__user__email"],
                "phone_number": attendee["student__phone_number"],
                "attended_at": attendee["attended_at"],
                "id": attendee["student__id"],
                "profile_pic": attendee["student__profile_pic"],
                "dept": attendee["student__dept"],
            }
            for attendee in attendees
        ]

    return render(
        request,
        "event/event_management.html",
        {"events": events, "data": data, "form": form, "members": members},
    )
