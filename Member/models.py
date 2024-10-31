from django.db import models
from django.forms import ValidationError
from django.http import request
from authentication.models import Student
from Dashboard.models import Club, Notice
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


class JoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "club")

    def __str__(self):
        return f"{self.student.student_id} - {self.club.club_name}"

    def get_total_request(self):
        return JoinRequest.objects.filter(status=False, club=self.club).count()

    def delete_joined_requests(self, *args, **kwargs):
        if self.status:  # Only if request is approved
            # Delete the corresponding notification
            Notification.objects.filter(
                notification_type=Notification.JOIN_REQUEST,
                club=self.club,
                Student=self.student.user,
            ).delete()
            # Then delete the join request
            self.delete()


class MemberJoined(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "club")

    def __str__(self):
        return f"{self.student.student_id} - {self.club.club_name}"


@receiver(post_save, sender=JoinRequest)
def create_member_joined(sender, instance, created, **kwargs):
    if instance.status:  # Only proceed if status is True
        MemberJoined.objects.get_or_create(student=instance.student, club=instance.club)


class Notification(models.Model):
    JOIN_REQUEST = "join_request"
    EVENTS = "events"
    NOTICES = "notices"

    CATEGORY_CHOICES = [
        (JOIN_REQUEST, "Join Request"),
        (EVENTS, "Events"),
        (NOTICES, "Notices"),
    ]
    ADMIN = "admin"
    GENERAL_USER = "general_user"

    USER_TYPES = [(ADMIN, "Admin"), (GENERAL_USER, "General User")]

    notification_type = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
    )

    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=100, choices=USER_TYPES, null=True, default=GENERAL_USER
    )
    Student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.Student) + " " + self.notification_type

    def notifications(self):
        return Notification.objects.filter(club=self.club).count()


@receiver(post_save, sender=JoinRequest)
def join_request_alert(sender, instance, *args, **kwargs):
    if instance.status == False:
        Notification.objects.create(
            notification_type="join_request",
            club=instance.club,
            user_type="admin",
            Student=instance.student.user,
        )


@receiver(post_save, sender=JoinRequest)
def delete_notification_on_approval(sender, instance, **kwargs):
    if instance.status:  # If the join request is approved
        # Delete the corresponding join request notification
        Notification.objects.filter(
            notification_type=Notification.JOIN_REQUEST,
            club=instance.club,
            Student=instance.student.user,
        ).delete()
        # Optionally, you could automatically delete the JoinRequest after approval
        instance.delete_joined_requests()


@receiver(post_save, sender=Notice)
def create_event_notification(sender, instance, **kwargs):
    if instance.read == False:
        members = [
            member.student for member in MemberJoined.objects.filter(club=instance.club)
        ]
        for i in members:
            Notification.objects.create(
                notification_type="notices",
                club=instance.club,
                user_type="general_user",
                Student=i.user,
            )


