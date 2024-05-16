from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Student
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
            return render(request, 'login.html') 
    
    else:
        return render(request, 'login.html')


def user_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = StudentForm()
        return render(request, 'login.html', {'form': form})
  
 
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
        form = StudentForm(request.POST, instance=students)
        if form.is_valid():
            form.save()
            print("Data Updated")
            return redirect('profile')
        else:
            print("Data Not Updated")
            return render(request, 'user_edit.html', {'form': form})
    
    return render(request, 'user_edit.html', {'form': form})