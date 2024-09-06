from rest_framework import serializers
from .models import Student, User


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None)

    class Meta:
        model = Student
        fields = "__all__"
