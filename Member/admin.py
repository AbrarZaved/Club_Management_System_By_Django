from django.contrib import admin
from .models import JoinRequest, MemberJoined, Notification
# Register your models here.
admin.site.register(MemberJoined)
admin.site.register(JoinRequest)
admin.site.register(Notification)
