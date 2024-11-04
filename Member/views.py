from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from authentication.models import Student
from Dashboard.models import Club
from .models import JoinRequest, MemberJoined, Notification
from django.contrib import messages
import json
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from authentication.serializer import StudentSerializer


# Create your views here.abs
def join_request(request):
    if request.method == "POST":
        student = Student.objects.get(user=request.user)
        club = Club.objects.get(club_name=request.POST["club_name"])
        
        if JoinRequest.objects.filter(student=student, club=club).exists():
            messages.info(request, "Request Already Sent")
            return redirect("club")
        else:
            join_request = JoinRequest(student=student, club=club)
            join_request.save()
            messages.success(request, "Request Sent")
            return redirect("club")

    return render(request, "dashboard/clubs.html")


def my_club(request):
    admin_name = request.user.username[6:]
    club_name = Club.objects.get(tag=admin_name)
    join_request = JoinRequest.objects.filter(club=club_name)

    if request.method == "POST":
        id_list = list(request.POST.getlist("status"))
        if id_list:
            for i in id_list:
                x = int(i)
                join_request = JoinRequest.objects.get(pk=x)
                # Update the status and save to trigger post_save signal
                join_request.status = True
                join_request.save()  # This will trigger the post_save signal
            messages.info(request, "Members Approved")
            return redirect("my_club")

    members = MemberJoined.objects.filter(club=club_name)
    return render(
        request,
        "member/my_club.html",
        {"join_request": join_request, "members": members},
    )


def view_member(request, boom):
    print(boom)
    students = Student.objects.get(id=boom)
    print(students)
    return render(request, "member/member_view.html", {"students": students})


def delete_member(request, boom):
    admin_name = request.user.username[6:]
    club_name = Club.objects.get(tag=admin_name)
    student = Student.objects.get(id=boom)
    member = MemberJoined.objects.get(student=student, club=club_name)
    member.delete()
    return redirect("my_club")


def search_member(request):
    admin_name = request.user.username[6:]
    club_name = Club.objects.get(tag=admin_name)

    if request.method == "POST":
        search = json.loads(request.body).get("searchText", "")
        search_parts = search.split()

        if len(search_parts) == 2:
            first_name, last_name = search_parts
            members = MemberJoined.objects.filter(
                Q(student__first_name__icontains=first_name)
                & Q(student__last_name__icontains=last_name)
                | Q(
                    student__first_name__icontains=search
                )  # Handles cases where the full name is in first name
                | Q(
                    student__last_name__icontains=search
                )  # Handles cases where the full name is in last name
                | Q(student__student_id__icontains=search),
                club=club_name,
            )
        else:
            members = MemberJoined.objects.filter(
                Q(student__first_name__icontains=search)
                | Q(student__last_name__icontains=search)
                | Q(student__student_id__icontains=search),
                club=club_name,
            )

        members = members.select_related("student", "club").values(
            "student__first_name",
            "student__last_name",
            "student__student_id",
            "club__club_name",
        )

        data = list(members)
        return JsonResponse(data, safe=False)
