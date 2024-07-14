from Dashboard.models import Club
from .models import JoinRequest, MemberJoined, Notification
from django.core.exceptions import ObjectDoesNotExist

def pending_requests_count(request):
    user = str(request.user)
    admin_name = user[6:]
    
    try:
        club = Club.objects.get(tag=admin_name)
        if "admin" in user:
            pending_requests_count = JoinRequest.objects.filter(status=False, club=club).count()
            pending_notifications_count = Notification.objects.all().count()
        else:
            pending_requests_count = 0
            pending_notifications_count = 0
    except ObjectDoesNotExist:
        pending_requests_count = 0
        pending_notifications_count = 0

    return {
        'pending_requests_count': pending_requests_count,
        'pending_notifications_count': pending_notifications_count,
    }
