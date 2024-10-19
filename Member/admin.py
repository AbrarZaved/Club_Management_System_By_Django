from django.contrib import admin
from .models import JoinRequest, MemberJoined, Notification


# Register your models here.
@admin.register(MemberJoined)
class MemberJoinedAdmin(admin.ModelAdmin):
    list_display = ["student", "club"]
    list_filter = ["club"]


admin.site.register(JoinRequest)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["Student", "notification_type", "club", "user_type"]
