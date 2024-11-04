from Dashboard.models import Club, Notice
from .models import JoinRequest, MemberJoined, Notification
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Student
from django.contrib.auth.models import AnonymousUser

def Alerts(request):
    user = str(request.user)
    is_admin = "admin" in user
    total_notifications = 0
    pending_joining_requests = 0
    pending_event_requests = 0
    pending_notices = []
    all_notices = 0

    if request.user.is_authenticated:
        if not is_admin:
            try:
                student = Student.objects.get(user=request.user)
                clubs = MemberJoined.objects.filter(student=student).values_list(
                    "club__club_name", flat=True
                )

                # Count all notices related to joined clubs
                all_notices = Notice.objects.filter(club__club_name__in=clubs).count()

                for club_name in clubs:
                    count = Notification.objects.filter(
                        club__club_name=club_name,
                        user_type="general_user",
                        Student__username=user,
                    ).count()

                    if count > 0:
                        pending_notices.append((count, club_name))
                        total_notifications += count

            except ObjectDoesNotExist:
                pass
        else:
            admin_name = user[6:]
            try:
                club = Club.objects.get(tag=admin_name)

                total_notifications = Notification.objects.filter(
                    club=club, user_type="admin"
                ).count()

                pending_joining_requests = Notification.objects.filter(
                    notification_type="join_request", club=club
                ).count()

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
        "all_notices": all_notices,
    }


def club_membership_status(request):
    club_list = Club.objects.all()
    club_status = {}

    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        # If the user is not authenticated, return empty club status
        return {"club_status": club_status}

    # Proceed with getting user clubs if authenticated
    user_clubs = MemberJoined.objects.filter(student__user=request.user).values_list(
        "club__club_name", flat=True
    )

    # Build the club status dictionary
    for club in club_list:
        club_status[club.club_name] = club.club_name in user_clubs

    return {"club_status": club_status}
