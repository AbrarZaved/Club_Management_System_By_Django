from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Club, Notice
from authentication.models import Student
from Member.models import Notification, MemberJoined, Status
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
        club_name = Club.objects.get(tag=admin_name)
        if request.method == "POST":
            Members = MemberJoined.objects.filter(club=club_name)
            title = request.POST["title"]
            description = request.POST["description"]
            Notice.objects.create(title=title, description=description, club=club_name)
            notice_count = Notice.objects.filter(club=club_name, read=False).count()
            for member in Members:
                Notification.objects.update_or_create(
                    notification_type="notices",
                    club=club_name,
                    user_type="general_user",
                    Student=member,
                    defaults={"total": notice_count},
                )
            messages.success(request, "Notice Added")
            return redirect("notice")
        else:
            form_data = {}
            total = Notice.objects.filter(club__club_name=club_name).count()
            total_id = list(
                Notice.objects.filter(club__club_name=club_name).values_list(
                    "id", flat=True
                )
            )

            print(total_id)
            if total_id:
                for i in total_id:
                    title = Notice.objects.get(id=i, club__club_name=club_name).title
                    description = Notice.objects.get(
                        id=i, club__club_name=club_name
                    ).description
                    form_data[title] = description
                print(form_data)
                return render(
                    request, "dashboard/notice.html", {"form_data": form_data}
                )

            return render(request, "dashboard/notice.html", {"form_data": form_data})
    else:
        form_data = {}

        clubs = MemberJoined.objects.filter(student=student).values_list(
            "club__club_name", flat=True
        )

        clubs_with_notices = []
        for club_name in clubs:
            if Notice.objects.filter(club__club_name=club_name).exists():
                clubs_with_notices.append(club_name)

        if clubs_with_notices:
            for club_name in clubs_with_notices:
                notices = Notice.objects.filter(club__club_name=club_name)

                for notice in notices:
                    form_data[notice.title] = notice.description

        updating = Status.objects.filter(student__student=student).update(total=0)
        data = Notification.objects.filter(
            Student__student=student, notification_type="notices"
        )
        for i in data:
            i.delete()

        return render(request, "dashboard/notice.html", {"form_data": form_data})


def delete_notice(request, title):
    admin_name = request.user.username[6:]
    club_name = Club.objects.get(tag=admin_name)
    form = Notice.objects.get(title=title, club=club_name)
    form.delete()
    return redirect("notice")


def search_clubs(request):
    if request.method == "POST":
        club_name = json.loads(request.body).get("text")
        data = Club.objects.filter(
            Q(club_name__icontains=club_name) | Q(tag=club_name)
        ).values("club_name", "image", "about_club", "club_link", "tag")

        return JsonResponse(list(data), safe=False)
