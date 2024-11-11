from django.shortcuts import render

from Event.forms import EventForm


# Create your views here.
def event(request):

    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "event/event.html")
    return render(request, "event/event.html", {"form": form})
