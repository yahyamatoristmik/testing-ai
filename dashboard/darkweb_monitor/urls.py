from django.urls import path
from . import views

app_name = 'darkweb_monitor'

urlpatterns = [
    path('dashboard/', views.darkweb_dashboard, name='dashboard'),
    path('submit-scan/', views.submit_darkweb_scan, name='submit_scan'),
    path('history/', views.darkweb_history, name='history'),
    path('scan/<int:scan_id>/', views.darkweb_scan_detail, name='scan_detail'),
]
