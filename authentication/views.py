from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.viewsets import ModelViewSet

from authentication.serializer import StudentSerializer
from .models import Student, UserRegistration
from .forms import StudentForm
from django.contrib.auth.models import User
from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)
        admin = str(user)
        if user is not None:
            login(request, user)
            try:
                obj = Student.objects.get(user=user)
                stu_id = obj.student_id
            except Student.DoesNotExist:
                stu_id = ""

            if stu_id == "" and admin != "admin":
                messages.info(request, "Login Successful. Please Complete Your Profile")
            else:
                messages.success(request, "Logged In Successfully")

            return redirect("dashboard")

        else:
            messages.error(request, "Invalid username or password")
            return render(request, "authentication/sign.html")

    else:
        return render(request, "authentication/sign_in.html")


def user_registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return redirect("register")
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        Student.objects.create(user=user, email=email)
        user.save()
        return redirect("login")
    else:
        return render(request, "authentication/sign_up.html")


def user_logout(request):
    logout(request)
    return redirect("home")


def user_profile(request):
    students = Student.objects.filter(user=request.user)
    return render(request, "authentication/user.html", {"students": students})


def user_edit(request, pk):
    students = Student.objects.get(pk=pk)
    form = StudentForm(instance=students)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=students)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = students.user
            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            return redirect("profile")
        else:
            return render(request, "authentication/user_edit.html", {"form": form})

    return render(request, "authentication/user_edit.html", {"form": form})


class memberList(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
