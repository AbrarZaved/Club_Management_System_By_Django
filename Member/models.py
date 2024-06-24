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
        unique_together = ('student', 'club')

    def __str__(self):
        return f'{self.student.student_id} - {self.club.club_name}'

class MemberJoined(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'club')

    def __str__(self):
        return f'{self.student.student_id} - {self.club.club_name}'

@receiver(post_save, sender=JoinRequest)
def create_member_joined(sender, instance, created, **kwargs):
    if instance.status:  # Only proceed if status is True
        MemberJoined.objects.get_or_create(
            student=instance.student,
            club=instance.club
        )
