from django.urls import path
from . import views

app_name = 'data_leak'

urlpatterns = [
    path('dashboard/', views.data_leak_dashboard, name='dashboard'),
    path('submit-scan/', views.submit_scan, name='submit_scan'),
    path('history/', views.scan_history, name='history'),
    path('scan/<int:scan_id>/', views.scan_detail, name='scan_detail'),
]
