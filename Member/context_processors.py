from Dashboard.models import Club
from .models import JoinRequest, MemberJoined, Notification
from django.core.exceptions import ObjectDoesNotExist


def pending_requests_count(request):
    user = str(request.user)
    admin_name = user[6:]

    try:
        club = Club.objects.get(tag=admin_name)
        if "admin" in user:
            total_notifications = Notification.objects.filter(club=club).count()
            pending_joining_requests = Notification.objects.filter(
                notification_type="join_request", club=club
            )
            pending_event_requests = Notification.objects.filter(
                notification_type="events", club=club
            )
            joining_requests = JoinRequest.objects.filter(club=club).count()
        else:
            total_notifications = 0
            joining_requests = 0
    except ObjectDoesNotExist:
        total_notifications = 0
        pending_joining_requests = 0
        joining_requests = 0
        pending_event_requests = 0
    return {
        "total_notifications": total_notifications,
        "pending_joining_requests": pending_joining_requests,
        "pending_event_requests": pending_event_requests,
        "joining_requests": joining_requests,
    }
