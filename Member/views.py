from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from authentication.models import Student
from Dashboard.models import Club
from .models import JoinRequest
from django.contrib import messages

# Create your views here.abs
def join_request(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        club = Club.objects.get(club_name=request.POST['club_name'])
        if JoinRequest.objects.filter(student=student,club=club).exists():
            messages.info(request,'Request Already Sent')
            return redirect('club')
        else:
            join_request = JoinRequest(student=student,club=club)
            join_request.save()
            messages.success(request,'Request Sent')
            return redirect('club')
        
    return render(request,'dashboard/clubs.html')


def my_club(request):
    student = request.user.username[6:]
    club_name = Club.objects.get(tag=student)
    join_request = JoinRequest.objects.filter(club=club_name)
    return render(request,'member/my_club.html',{'join_request':join_request})
        