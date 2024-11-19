from django.contrib import admin
from .models import Event, EventAttender


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "event_club", "event_time"]
    list_filter = ["event_club"]


@admin.register(EventAttender)
class EventAttenderAdmin(admin.ModelAdmin):
    list_display = ["id","event", "student", "is_going"]
    list_filter = ["is_going"]
