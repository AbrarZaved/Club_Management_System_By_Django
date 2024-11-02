from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Club, Notice
from authentication.models import Student
from Member.models import Notification, MemberJoined
from django.http import HttpResponse, JsonResponse
import json
from django.db.models import Q


def home(request):
    return render(request, "dashboard/index.html")


def dashboard(request):
    user = request.user
    student = Student.objects.get(user=user)

    # Get club names the student has joined
    clubs = MemberJoined.objects.filter(student=student).values_list(
        "club__club_name", flat=True
    )

    # Fetch recent notices for these clubs
    clubs_with_notices = (
        Notice.objects.filter(club__club_name__in=clubs)
        .order_by("-created_at")  # Order by latest first
        .select_related("club")
        .values("title", "club__club_name", "created_at","id")[:3]  # Get the latest 3
    )
    recent_notices = {}
    # Format data for rendering
    for notice in clubs_with_notices:
        unique_key = f"{notice['title']}_{notice['created_at'].strftime('%B %d, %Y at %I:%M %p')}"
        recent_notices[unique_key] = {
            "club": notice["club__club_name"],
            "time": notice["created_at"].strftime("%B %d, %Y at %I:%M %p"),
            "id": notice["id"],
        }

    return render(
        request, "dashboard/dashboard.html", {"recent_notices": recent_notices}
    )


def add_event(request):
    return render(request, "dashboard/add_event.html")


def club_list(request):
    club = Club.objects.all()
    return render(request, "dashboard/clubs.html", {"club": club})


@login_required
def notice(request,pk=None):
    user = request.user
    student = Student.objects.get(user=user)
    form_data = {}

    if "admin" in str(user):
        # Admin logic
        club = Club.objects.get(tag=user.username[6:])

        if request.method == "POST":
            title, description = request.POST["title"], request.POST["description"]
            Notice.objects.create(title=title, description=description, club=club)
            messages.success(request, "Notice Added")
            return redirect("notice")

        # Fetch notices for the admin's club
        notices = Notice.objects.filter(club=club).values(
            "id", "title", "description", "club__club_name", "created_at", "id"
        )
        for notice in notices:
            unique_key = f"{notice['title']}_{notice['created_at'].strftime('%B %d, %Y at %I:%M %p')}"
            form_data[unique_key] = {
                "description": notice["description"],
                "club": notice["club__club_name"],
                "time": notice["created_at"].strftime("%B %d, %Y at %I:%M %p"),
                "id": notice["id"],
            }

    else:
        # Member logic
        clubs = MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )
        clubs_with_notices = (
            Notice.objects.filter(club__club_name__in=clubs)
            .select_related("club")
            .values("title", "description", "club__club_name", "created_at","id")
        )
        print(len(clubs_with_notices))
        for notice in clubs_with_notices:
            unique_key = f"{notice['title']}_{notice['created_at'].strftime('%B %d, %Y at %I:%M %p')}"
            form_data[unique_key] = {
                "description": notice["description"],
                "club": notice["club__club_name"],
                "time": notice["created_at"].strftime(
                    "%B %d, %Y at %I:%M %p"
                ),  # Updated to desired format
                "id": notice["id"],
            }

        # Sort by creation time in descending order
        print(len(form_data))
        form_data = dict(
            sorted(form_data.items(), key=lambda item: item[1]["time"], reverse=True)
        )
        print(len(form_data))
        # Clear notifications for this user
        Notification.objects.filter(Student__username=str(user)).delete()

        # Get counts of notices per club
        clubs_with_notice = [
            (club, Notice.objects.filter(club__club_name=club).count())
            for club in clubs
        ]

    return render(
        request,
        "dashboard/notice.html",
        {
            "form_data": form_data,
            "clubs_with_notices": (
                clubs_with_notice if "admin" not in str(user) else None
            ),
        },
    )


def delete_notice(request, boom):
    form = Notice.objects.get(id=boom)
    form.delete()
    return redirect("notice")


def search_clubs(request):
    if request.method == "POST":
        club_name = json.loads(request.body).get("text")
        data = Club.objects.filter(
            Q(club_name__icontains=club_name) | Q(tag=club_name)
        ).values("club_name", "image", "about_club", "club_link", "tag")

        return JsonResponse(list(data), safe=False)


def filter_notices(request):
    if request.method == "POST":
        club_name = json.loads(request.body).get("text")
        meta_data = Notice.objects.filter(club__club_name=club_name)
        data = [
            {
                "id": notice.id,
                "title": notice.title,
                "description": notice.description,
                "club_name": notice.club.club_name,
                "created_at": notice.created_at,
            }
            for notice in meta_data
        ]
        return JsonResponse(data, safe=False)
