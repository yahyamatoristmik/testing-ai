from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('message/', include('message.urls')),
    path('dast-reports/', include(('dast_reports.urls', 'dast_reports'), namespace='dast_reports')),
    path('sast-report/', include('sast_report.urls')),
    
    # Authentication - PAKAI INI
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('data-leak/', include('data_leak.urls')),  # ✅ PASTIKAN INI ADA
    path('darkweb-monitor/', include('darkweb_monitor.urls')), 
]
