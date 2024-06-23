from django.db import models
from authentication.models import Student
from Dashboard.models import Club

class JoinRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'club')
    
    def __str__(self):
        return f'{self.student.student_id} - {self.club.club_name}'
