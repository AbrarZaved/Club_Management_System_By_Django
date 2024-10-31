from django.contrib import admin
from .models import Club, Notice

admin.site.register(Club)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["club", "title", "created_at"]
    list_filter = ["club"]
