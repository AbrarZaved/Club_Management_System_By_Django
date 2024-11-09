from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("club_list", views.club_list, name="club"),
    path("notice", views.notice, name="notice"),
    path("notice/<int:pk>", views.notice, name="notice"),
    path("delete_notice/<int:boom>", views.delete_notice, name="delete"),
    path("", views.home, name="home"),
    path("club_properties", csrf_exempt(views.club_properties), name="club_properties"),
    path("notice_properties", csrf_exempt(views.notice_properties), name="notice_properties"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
