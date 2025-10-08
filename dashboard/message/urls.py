# ==========================================
# message/urls.py
# ==========================================
from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('contact/', views.contact_view, name='contact_form'),
    path('success/', views.success_view, name='success'),
]
