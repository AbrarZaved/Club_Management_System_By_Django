from django.shortcuts import render,redirect
from .forms import NoticeForm
from django.contrib.auth.decorators import login_required
from .models import Club,Notice
from authentication.models import Student



def dashboard(request):      
    return render(request,'dashboard.html')

def add_event(request):      
    return render(request,'add_event.html')





def club_list(request):
    club = Club.objects.all()
    return render(request, 'clubs.html',{"club":club})

@login_required
def notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice')
        else:
            return render(request,'notice.html',{"form":form})
    else:
        form_data = Notice.objects.all()
        form = NoticeForm()
        return render(request, 'notice.html',{"form":form,"form_data":form_data})
    
def delete_notice(request,notice_id):
    form = Notice.objects.get(pk=notice_id)
    form.delete()
    return redirect('notice')
    