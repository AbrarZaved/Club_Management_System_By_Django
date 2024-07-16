from Dashboard.models import Club
from .models import JoinRequest, MemberJoined, Notification
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Student
from Dashboard.models import Notice


def Alerts(request):
    user = str(request.user)
    admin_name = user[6:]
    total_notifications = 0
    pending_joining_requests = 0
    pending_event_requests = 0
    pending_notices = 0
    club = 0
    clubs = 0
    clubing = 0
    student = 0
    total_data = 0
    if request.user.is_authenticated and "admin" not in user:
        student = Student.objects.get(user=request.user)

    try:
        if "admin" in user:
            club = Club.objects.get(tag=admin_name)
            print("Admin Detected")
            total_notifications = Notification.objects.filter(club=club).count()
            pending_joining_requests = Notification.objects.filter(
                notification_type="join_request", club=club
            )
            pending_event_requests = Notification.objects.filter(
                notification_type="events", club=club
            )

        else:
            clubs = list(MemberJoined.objects.filter(student=student))
            clubing = [i.club.club_name for i in clubs]
            print(clubing)
            for i in clubing:
                total_data = Notice.objects.filter(club__club_name=i).count()
                if total_data == 0:
                    clubing.remove(i)
            print(clubing,total_data)
            if clubing:
                for i in clubing:
                    total_notifications += Notification.objects.filter(
                        club__club_name=i
                    ).count()

            pending_notices = Notification.objects.filter(
                notification_type="notices", club=club
            )

    except ObjectDoesNotExist:
        pass

    return {
        "total_notifications": total_notifications,
        "pending_joining_requests": pending_joining_requests,
        "pending_event_requests": pending_event_requests,
        "pending_notices": pending_notices,
    }
