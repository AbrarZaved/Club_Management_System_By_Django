from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Club, Notice
from authentication.models import Student
from Member.models import Notification, MemberJoined
from django.http import HttpResponse, JsonResponse
import json
from django.db.models import Q
from zoneinfo import ZoneInfo


def format_time_dhaka(time):
    # Convert to Dhaka timezone using zoneinfo
    dhaka_tz = ZoneInfo("Asia/Dhaka")
    local_time = time.astimezone(dhaka_tz)
    return local_time.strftime("%B %d, %Y at %I:%M %p")


def home(request):
    return render(request, "dashboard/index.html")


def dashboard(request):
    admin_name = request.user.username[6:]
    user = request.user
    student = Student.objects.get(user=user)

    if "admin" in str(user):
        club_name = Club.objects.get(tag=admin_name)
        clubs_with_notices = (
            Notice.objects.filter(club__club_name=club_name)
            .order_by("-created_at")  # Order by latest first
            .select_related("club")
            .values("title", "club__club_name", "created_at", "id")[
                :3
            ]  # Get the latest 3
        )
        recent_notices = {}
        # Format data for rendering
        for notice in clubs_with_notices:
            unique_key = f"{notice['title']}_{notice['created_at'].strftime('%B %d, %Y at %I:%M %p')}"
            recent_notices[unique_key] = {
                "club": notice["club__club_name"],
                "time": format_time_dhaka(notice["created_at"]),
                "id": notice["id"],
            }

        return render(
            request, "dashboard/dashboard.html", {"recent_notices": recent_notices}
        )
    # Get club names the student has joined
    clubs = MemberJoined.objects.filter(student=student).values_list(
        "club__club_name", flat=True
    )

    # Fetch recent notices for these clubs
    clubs_with_notices = (
        Notice.objects.filter(club__club_name__in=clubs)
        .order_by("-created_at")  # Order by latest first
        .select_related("club")
        .values("title", "club__club_name", "created_at", "id")[:3]  # Get the latest 3
    )
    recent_notices = {}
    # Format data for rendering
    for notice in clubs_with_notices:
        unique_key = f"{notice['title']}_{notice['created_at'].strftime('%B %d, %Y at %I:%M %p')}"
        recent_notices[unique_key] = {
            "club": notice["club__club_name"],
            "time": format_time_dhaka(notice["created_at"]),
            "id": notice["id"],
        }

    return render(
        request, "dashboard/dashboard.html", {"recent_notices": recent_notices}
    )


def club_list(request):
    club = Club.objects.all()
    return render(request, "dashboard/clubs.html", {"club": club})


@login_required
def notice(request, pk=None):
    admin_name = request.user.username[6:]
    user = str(request.user)
    student = Student.objects.get(user=request.user)
    print(user)

    if "admin" in user:
        club_name = Club.objects.get(tag=admin_name)
        if request.method == "POST":
            print("Creating fbdsfsdkhf")
            title = request.POST["title"]
            description = request.POST["description"]
            Notice.objects.create(title=title, description=description, club=club_name)
            messages.success(request, "Notice Added")
            return redirect("notice")

    else:
        # Member logic
        clubs = MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )
        clubs_with_notices = (
            Notice.objects.filter(club__club_name__in=clubs)
            .select_related("club")
            .values("title", "description", "club__club_name", "created_at", "id")
        )

        # Clear notifications for this user
        Notification.objects.filter(
            Student__username=str(user), notification_type="notices"
        ).delete()

        # Get counts of notices per club
        clubs_with_notice = [
            (club, Notice.objects.filter(club__club_name=club).count())
            for club in clubs
        ]

    return render(
        request,
        "dashboard/notice.html",
        {
            "clubs_with_notices": (
                clubs_with_notice if "admin" not in str(user) else None
            ),
        },
    )


def delete_notice(request, boom):
    form = Notice.objects.get(id=boom)
    form.delete()
    return redirect("notice")


def club_properties(request):
    if request.method == "POST":
        user = request.user
        student = Student.objects.get(user=user)
        selectedClub = json.loads(request.body).get("selectedClub")
        club_name = json.loads(request.body).get("text")
        if selectedClub:
            data = {}
            if selectedClub == "joined":
                meta_data = MemberJoined.objects.filter(student=student).values_list(
                    "club__club_name",
                    "club__image",
                    "club__about_club",
                    "club__club_link",
                    "club__tag",
                )
                data = [
                    {
                        "club_name": club[0],
                        "image": club[1],
                        "about_club": club[2],
                        "club_link": club[3],
                        "tag": club[4],
                    }
                    for club in meta_data
                ]
                return JsonResponse(list(data), safe=False)
            if selectedClub == "explore":
                data = {}
                club_list = list(
                    Club.objects.values_list("club_name", flat=True)
                )  # Directly convert to list
                member_clubs = list(
                    MemberJoined.objects.filter(student=student).values_list(
                        "club__club_name", flat=True
                    )
                )  # Use flat=True to get a flat list of club names
                for i in [
                    club for club in club_list if club not in member_clubs
                ]:  # Filter `club_list` to only items not in `member_clubs`
                    meta_data = Club.objects.filter(club_name=i).values_list(
                        "club_name",
                        "image",
                        "about_club",
                        "club_link",
                        "tag",
                    )
                data = [
                    {
                        "club_name": club[0],
                        "image": club[1],
                        "about_club": club[2],
                        "club_link": club[3],
                        "tag": club[4],
                    }
                    for club in meta_data
                ]
                return JsonResponse(list(data), safe=False)
            if (
                selectedClub == "All"
            ):  # Filter `club_list` to only items not in `member_clubs`
                meta_data = Club.objects.all().values_list(
                    "club_name",
                    "image",
                    "about_club",
                    "club_link",
                    "tag",
                )
                data = [
                    {
                        "club_name": club[0],
                        "image": club[1],
                        "about_club": club[2],
                        "club_link": club[3],
                        "tag": club[4],
                    }
                    for club in meta_data
                ]
                return JsonResponse(list(data), safe=False)
        if club_name:
            data = Club.objects.filter(
                Q(club_name__icontains=club_name) | Q(tag=club_name)
            ).values("club_name", "image", "about_club", "club_link", "tag")

            return JsonResponse(list(data), safe=False)


def notice_properties(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # Parse request body
    data = json.loads(request.body)
    club_name = data.get("text")
    search_value = data.get("search_value")
    user = request.user

    # Check if the user is a student or an admin
    if "admin" in str(user):
        # Admin logic: Extract club based on the admin's username (assumes admin username format)
        club_tag = user.username[6:]
        club = Club.objects.get(tag=club_tag)

        # Fetch notices for the admin's club
        notices = Notice.objects.filter(club=club).values(
            "id", "title", "description", "club__club_name", "created_at"
        )
        form_data = [
            {   "is_admin": True,
                "id": notice["id"],
                "title": notice["title"],
                "description": notice["description"],
                "club_name": notice["club__club_name"],
                "created_at": format_time_dhaka(notice["created_at"]),
            }
            for notice in notices
        ]
        form_data.sort(key=lambda x: x["created_at"], reverse=True)
        return JsonResponse(form_data, safe=False)

    # If user is a student, fetch their clubs
    student = Student.objects.get(user=user)
    clubs = MemberJoined.objects.filter(student=student).values_list(
        "club__club_name", flat=True
    )

    # Search functionality for students
    if search_value:
        meta_data = Notice.objects.filter(
            Q(club__club_name__icontains=search_value)
            | Q(title__icontains=search_value)
            | Q(description__icontains=search_value)
            | Q(club__tag__icontains=search_value)
        ).values(
            "id", "title", "description", "club__club_name", "club__tag", "created_at"
        )
        data = [
            {
                "id": notice["id"],
                "title": notice["title"],
                "description": notice["description"],
                "club_name": notice["club__club_name"],
                "created_at": format_time_dhaka(notice["created_at"]),
                "tag": notice["club__tag"],
            }
            for notice in meta_data
        ]
        return JsonResponse(data, safe=False)

    # Fetch notices for "All" clubs or a specific club
    if club_name:
        notices = Notice.objects.filter(
            club__club_name__in=clubs if club_name == "All" else [club_name]
        ).values("id", "title", "description", "club__club_name", "created_at")
        data = [
            {
                "id": notice["id"],
                "title": notice["title"],
                "description": notice["description"],
                "club_name": notice["club__club_name"],
                "created_at": format_time_dhaka(notice["created_at"]),
            }
            for notice in notices
        ]
        # Sort by creation date if "All" clubs are selected
        data.sort(key=lambda x: x["created_at"], reverse=True)
        if club_name == "All":
            data.sort(key=lambda x: x["created_at"], reverse=True)
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid data"}, status=400)
