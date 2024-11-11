from django import forms
from Event.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "is_read": forms.HiddenInput(),
            "event_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",  # Faded gray underline
                }
            ),
            "event_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "event_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "event_location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "event_description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "event_link": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "event_club": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "created_at": forms.HiddenInput(),
            "event_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "style": "color: black; border-bottom: 2px solid rgba(0, 0, 0, 0.2);",
                }
            ),
            "updated_at": forms.HiddenInput(),
        }
