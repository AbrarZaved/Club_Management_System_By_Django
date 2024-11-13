import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from Dashboard.models import Club
from authentication.models import Student
from django.apps import apps


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    event_description = models.TextField()
    event_image1 = models.ImageField(
        upload_to="event_image", blank=True, default="profile_pic/new_logo.png"
    )
    event_image2 = models.ImageField(
        upload_to="event_image", blank=True, default="profile_pic/new_logo.png"
    )
    event_image3 = models.ImageField(
        upload_to="event_image", blank=True, default="profile_pic/new_logo.png"
    )
    event_link = models.URLField(blank=True, null=True)
    event_club = models.ForeignKey(Club, verbose_name="Club", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False, verbose_name="Read")

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        # Resize the images to 800x800 before saving
        if self.event_image1:
            self.event_image1 = self.resize_image(self.event_image1)

        if self.event_image2:
            self.event_image2 = self.resize_image(self.event_image2)

        if self.event_image3:
            self.event_image3 = self.resize_image(self.event_image3)

        super().save(*args, **kwargs)

    def resize_image(self, image_field, size=(800, 550)):
        # Open the image using Pillow
        img = Image.open(image_field)

        # Resize the image to exactly 800x800 (distortion might occur if aspect ratio is not 1:1)
        img = img.resize(size, Image.Resampling.LANCZOS)

        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # Save the resized image to an in-memory file
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG")
        img_io.seek(0)

        # Create a new InMemoryUploadedFile from the resized image
        image_name = image_field.name.split("/")[-1]
        image_field = InMemoryUploadedFile(
            img_io, None, image_name, "image/jpeg", img_io.tell(), None
        )
        return image_field


class EventAttender(models.Model):
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, verbose_name="Student", on_delete=models.CASCADE
    )
    is_going = models.BooleanField(default=False)
    attended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "student")  # Prevent duplicate entries
        ordering = ["-attended_at"]  # Most recent attendees first

    def __str__(self):
        return f"{self.student} - {self.event.event_name}"


@receiver(post_save, sender=Event)
def create_event_notifications(sender, instance, *args, **kwargs):
    MemberJoined = apps.get_model("Member", "MemberJoined")
    Notification = apps.get_model("Member", "Notification")
    if instance.is_read == False:
        member = [
            member.student
            for member in MemberJoined.objects.filter(club=instance.event_club)
        ]
        for i in member:
            Notification.objects.create(
                notification_type="events",
                club=instance.event_club,
                user_type="general_user",
                Student=i.user,
                event=instance,
            )


@receiver(post_delete, sender=Event)
def delete_event_notifications(sender, instance, *args, **kwargs):
    Notification = apps.get_model("Member", "Notification")
    if instance.is_read:
        Notification.objects.filter(id=instance.id).delete()
