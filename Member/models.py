from django.db import models
from authentication.models import Student
from Dashboard.models import Club


class JoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.student.student_id)+' '+ self.club.club_name