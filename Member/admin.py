from django.contrib import admin
from .models import JoinRequest, MemberJoined
# Register your models here.
admin.site.register(MemberJoined)
admin.site.register(JoinRequest)
