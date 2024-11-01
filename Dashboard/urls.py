from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("club_list", views.club_list, name="club"),
    path("notice", views.notice, name="notice"),
    path("add_event", views.add_event, name="event"),
    path("delete_notice/<int:boom>", views.delete_notice, name="delete"),
    path("", views.home, name="home"),
    path("search_clubs", csrf_exempt(views.search_clubs), name="search_clubs"),
    path("filter_notices", csrf_exempt(views.filter_notices), name="filter_notices"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
