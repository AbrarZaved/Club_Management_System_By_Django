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
    return render(request, "dashboard/dashboard.html")


def add_event(request):
    return render(request, "dashboard/add_event.html")


def club_list(request):
    club = Club.objects.all()
    return render(request, "dashboard/clubs.html", {"club": club})


@login_required
def notice(request):

    admin_name = request.user.username[6:]
    user = str(request.user)
    student = Student.objects.get(user=request.user)

    if "admin" in user:
        club = Club.objects.get(tag=admin_name)

        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]

            # Create a new notice for the club
            Notice.objects.create(title=title, description=description, club=club)
            messages.success(request, "Notice Added")
            return redirect("notice")

        else:
            # Fetch all notices for the club in a single query, including IDs
            notices = Notice.objects.filter(club=club).values(
                "id", "title", "description", "club__club_name"
            )
            form_data = {
                notice["title"]: {
                    "id": notice["id"],
                    "description": notice["description"],
                    "club": notice["club__club_name"],
                }
                for notice in notices
            }
            print(form_data)

            return render(request, "dashboard/notice.html", {"form_data": form_data})

    else:
        form_data = {}
        clubs = MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )

        # Fetch notices only for clubs with existing notices and store in form_data
        clubs_with_notices = (
            Notice.objects.filter(club__club_name__in=clubs)
            .select_related("club")
            .values("title", "description", "club__club_name", "created_at")
        )

        form_data = {
            notice["title"]: {
                "description": notice["description"],
                "club": notice["club__club_name"],
                "time": notice["created_at"],
            }
            for notice in clubs_with_notices
        }
        form_data = dict(
            sorted(form_data.items(), key=lambda item: item[1]["time"], reverse=True)
        )

        # Delete all notifications for the student
        Notification.objects.filter(Student__username=user).delete()

        # Prepare club notice counts
        clubs_with_notice = [
            (club_name, Notice.objects.filter(club__club_name=club_name).count())
            for club_name in clubs
            if Notice.objects.filter(club__club_name=club_name).exists()
        ]

        return render(
            request,
            "dashboard/notice.html",
            {"form_data": form_data, "clubs_with_notices": clubs_with_notice},
        )


def delete_notice(request, boom):
    admin_name = request.user.username[6:]
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
                "created_at":notice.created_at,
            }
            for notice in meta_data
        ]
        return JsonResponse(data, safe=False)
