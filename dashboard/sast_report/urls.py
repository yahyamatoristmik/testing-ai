from django.urls import path
from . import views

app_name = 'sast_report'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('scm-profiles/', views.scm_profiles, name='scm_profiles'),
    path('repositories/', views.repositories, name='repositories'),
    path('scan/<int:repo_id>/', views.start_scan, name='start_scan'),
    path('results/<int:scan_id>/', views.scan_results, name='scan_results'),
    path('history/', views.scan_history, name='scan_history'),
    path('api/status/<int:scan_id>/', views.scan_status_api, name='scan_status_api'),
]
