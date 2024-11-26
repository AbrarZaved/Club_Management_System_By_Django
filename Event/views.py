import json
from django.db.models import Q
from django.db.models.lookups import IContains
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Dashboard.models import Club
from Event.forms import EventForm
from Event.models import Event, EventAttender
from Member.models import MemberJoined, Notification
from authentication.models import Student


# Create your views here.
def event(request, pk=None):

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
            if form.is_valid():
                form.save()
                return redirect("event")
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

    return render(
        request,
        "event/event_management.html",
        {"form": form},
    )


def delete_event_attendee(request, attendee_id, event_name):
    if request.method == "DELETE":
        try:
            attendee = EventAttender.objects.get(
                student__student_id=attendee_id,
                event__event_name=event_name,
            )
            attendee.delete()
            return JsonResponse(
                {"message": "Attendee deleted successfully"}, status=200
            )
        except EventAttender.DoesNotExist:
            return JsonResponse({"error": "Attendee not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def event_properties(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    admin_name = request.user.username[6:]
    club = get_object_or_404(Club, tag=admin_name)

    # Fetch events for the club
    events = Event.objects.filter(event_club=club).select_related("event_club")
    data = []

    for event in events:
        attendees = (
            EventAttender.objects.filter(event=event)
            .select_related("student__user")
            .values(
                "student__user__first_name",
                "student__user__last_name",
                "student__student_id",
                "student__user__email",
                "student__phone_number",
                "attended_at",
                "student__profile_pic",
                "student__dept",
            )
        )

        # Prepare the data for each event
        event_data = {
            "event_name": event.event_name,
            "total_count": len(attendees),
            "attendees": [
                {
                    "full_name": f"{attendee['student__user__first_name']} {attendee['student__user__last_name']}",
                    "student_id": attendee["student__student_id"],
                    "email": attendee["student__user__email"],
                    "phone_number": attendee["student__phone_number"],
                    "attended_at": attendee["attended_at"],
                    "profile_pic": attendee["student__profile_pic"],
                    "dept": attendee["student__dept"],
                }
                for attendee in attendees
            ],
        }
        data.append(event_data)

    return JsonResponse(data, safe=False)


def event_search(request):
    search_text = json.loads(request.body).get("text", "")
    admin_name = request.user.username[6:]

    if "admin" in str(request.user):
        club = get_object_or_404(Club, tag=admin_name)
        events = Event.objects.filter(
            Q(event_name__icontains=search_text), event_club=club
        )
    else:
        user = request.user
        student = Student.objects.get(user=user)
        clubs = MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )
        events = Event.objects.filter(
            Q(event_name__icontains=search_text), event_club__club_name__in=clubs
        )

    data = list(
        events.values(
            "id",
            "event_name",
            "event_date",
            "event_time",
            "event_location",
            "event_description",
            "event_club",
            "event_image1",
            "event_image2",
            "event_image3",
            "event_link",
        )
    )
    return JsonResponse(data, safe=False)


def event_filter(request, pk=None):
    if request.method == "POST":
        user = request.user
        admin_name = request.user.username[6:]
        student = Student.objects.get(user=user)
        selected_club = json.loads(request.body).get("selectedClub")

        if "admin" in str(request.user):
            club = get_object_or_404(Club, tag=admin_name)
            events = Event.objects.filter(event_club=club)
        elif selected_club == "All Events":
            clubs = MemberJoined.objects.filter(student=student).values_list(
                "club__club_name", flat=True
            )
            events = Event.objects.filter(event_club__club_name__in=clubs)
        else:
            events = Event.objects.filter(event_club__club_name=selected_club)

        data = list(
            events.values(
                "id",
                "event_name",
                "event_date",
                "event_time",
                "event_location",
                "event_description",
                "event_club",
                "event_image1",
                "event_image2",
                "event_image3",
                "event_link",
            )
        )
        return JsonResponse(data, safe=False)
