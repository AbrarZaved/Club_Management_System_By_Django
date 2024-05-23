from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Student,UserRegistration
from .forms import StudentForm
from django.contrib.auth.models import User

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request, 'sign.html') 
    
    else:
        return render(request, 'sign.html')


def user_registration(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = User.objects.create_user(username=username,password=password,email=email)
        Student.objects.create(user=user)
        user.save()
        return redirect('login')
    else:
        return render(request, 'sign_up.html')
  
 
def user_logout(request):
    logout(request)
    return redirect('login')



def user_profile(request):
    students = Student.objects.filter(user=request.user)
    return render(request,'user.html',{"students":students})


def user_edit(request,pk):
    students = Student.objects.get(pk=pk)
    form = StudentForm(instance=students)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=students)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = students.user
            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            return redirect('profile')
        else:
            return render(request, 'user_edit.html', {'form': form})
    
    return render(request, 'user_edit.html', {'form': form})