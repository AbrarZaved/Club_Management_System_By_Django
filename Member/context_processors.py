from Dashboard.models import Club, Notice
from .models import JoinRequest, MemberJoined, Notification
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Student


def Alerts(request):
    user = str(request.user)
    admin_name = user[6:]
    total_notifications = 0
    pending_joining_requests = 0
    pending_event_requests = 0
    pending_notices = 0

    if request.user.is_authenticated and "admin" not in user:
        try:
            student = Student.objects.get(user=request.user)
            clubs = list(MemberJoined.objects.filter(student=student))
            clubing = [i.club.club_name for i in clubs]
            for i in clubing:
                total_data = Notice.objects.filter(club__club_name=i).count()
                if total_data == 0:
                    clubing.remove(i)
            if clubing:
                for i in clubing:
                    total_notifications += Notification.objects.filter(
                        club__club_name=i,user_type="general_user"
                    ).count()
            pending_notices = Notification.objects.filter(
                notification_type="notices", club__club_name__in=clubing
            )
        except ObjectDoesNotExist:
            pass
    elif "admin" in user:
        try:
            club = Club.objects.get(tag=admin_name)
            total_notifications = Notification.objects.filter(club=club,user_type="admin").count()
            pending_joining_requests = Notification.objects.filter(
                notification_type="join_request", club=club
            )
            pending_event_requests = Notification.objects.filter(
                notification_type="events", club=club
            ).count()
        except ObjectDoesNotExist:
            pass

    return {
        "total_notifications": total_notifications,
        "pending_joining_requests": pending_joining_requests,
        "pending_event_requests": pending_event_requests,
        "pending_notices": pending_notices,
    }
