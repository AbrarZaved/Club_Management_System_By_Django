from django import forms
from .models import Notice
from django.contrib.auth.forms import UserCreationForm

class NoticeForm(forms.ModelForm):
    
    class Meta:
        model = Notice
        fields = ['title','description']
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}), 
        }
