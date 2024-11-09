from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from authentication.views import memberList


router = DefaultRouter()
router.register("memberList", memberList, basename="member")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Dashboard.urls")),
    path("auth/", include("authentication.urls")),
    path("member/", include("Member.urls")),
    path("event/", include("Event.urls")),
    path("all/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
