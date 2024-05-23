from django.db import models
from django.contrib.auth.models import User


class UserRegistration(User):
    
    def __str__(self):
        return self.username

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=User)
    first_name = models.CharField(max_length=30,blank=False)
    last_name = models.CharField(max_length=30,blank=False)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True,default='profile_pic/new_logo.png')
    student_id = models.CharField(max_length=20,unique=True,blank=False)
    email = models.EmailField(unique=True)
    dept = models.CharField(max_length=30,blank=False)
    phone_number = models.CharField(max_length=15,unique=True,blank=False)
    batch = models.CharField(max_length=5,blank=False)
    address = models.CharField(max_length=70,blank=False)
    about_you = models.CharField(max_length=250, blank=True, null=True)

    
    def __str__(self):
        return self.student_id