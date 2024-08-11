from django.db import models
from authentication.models import Student
from Dashboard.models import Club
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    total = models.IntegerField(default=0)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100, choices=USER_TYPES,null=True,default=GENERAL_USER)
    Student = models.ForeignKey(MemberJoined,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return str(self.Student)+" "+self.notification_type

    def notifications(self):
        return Notification.objects.filter(club=self.club).count()


class Status(models.Model):
    student = models.ForeignKey(MemberJoined, verbose_name="Students", on_delete=models.CASCADE)
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student)