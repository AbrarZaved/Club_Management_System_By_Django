from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.user_login,name='login'),
    path('',views.user_registration,name='register'),
    path('user_logout', views.user_logout,name='logout'),
    path('user_edit/<int:pk>', views.user_edit,name='user_edit'),
    path('user_profile', views.user_profile,name='profile'),
  
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
