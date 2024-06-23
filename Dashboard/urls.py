from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard', views.dashboard,name='dashboard'),  
    path('club_list',views.club_list,name='club'),
    path('notice',views.notice,name='notice'),
    path('add_event',views.add_event,name='event'),
    path('delete_notice/<notice_id>',views.delete_notice,name='delete'),
    path('',views.home,name='home'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
