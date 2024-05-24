from django.urls import path
from . import views
from authentication import views as auth_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard', views.dashboard,name='dashboard'),  
    path('club_list',views.club_list,name='club'),
    path('notice',views.notice,name='notice'),
    path('add_event',views.add_event,name='event'),
    path('delete_notice/<notice_id>',views.delete_notice,name='delete'),
    path('',views.home,name='home'),
    path('sign', auth_view.user_login,name='login'),
    path('sign_up',auth_view.user_registration,name='register'),
    path('user_logout', auth_view.user_logout,name='logout'),
    path('user_edit/<int:pk>', auth_view.user_edit,name='user_edit'),
    path('user_profile', auth_view.user_profile,name='profile'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
