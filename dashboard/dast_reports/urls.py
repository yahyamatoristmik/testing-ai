# dast_reports/urls.py
from django.urls import path
from . import views

app_name = 'dast_reports'

urlpatterns = [
    path('scan/<int:scan_id>/generate-ai-recommendations/', views.generate_ai_recommendations, name='generate_ai_recommendations'),
    path('scan/<int:scan_id>/report/', views.scan_report_view, name='scan_report'),
    path('scan/<int:scan_id>/trigger/', views.trigger_zap_scan_view, name='trigger_scan'),
    path('scan/<int:scan_id>/ai-recommendations/', views.ai_recommendations_view, name='ai_recommendations'),
    path('public-report/<int:scan_id>/<str:token>/', views.public_ai_report_view, name='public_ai_report'),
    path('check-running-scans/', views.check_running_scans, name='check_running_scans'),
    # ⛔ HAPUS BARIS INI: path('test/', views.test_view, name='test_view'),
]
