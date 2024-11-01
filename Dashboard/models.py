from xmlrpc.client import DateTime
from django.db import models


class Club(models.Model):
    club_name = models.CharField(max_length=50, unique=True, blank=False)
    image = models.ImageField(
        upload_to="club_image", height_field=None, width_field=None, max_length=None
    )
    about_club = models.CharField(max_length=200, blank=False)
    club_link = models.URLField(max_length=200, unique=True)
    tag = models.CharField(max_length=10, blank=False, unique=True, default="")

    def __str__(self):
        return self.club_name


class Notice(models.Model):
    title = models.CharField(max_length=50)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=2000)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
