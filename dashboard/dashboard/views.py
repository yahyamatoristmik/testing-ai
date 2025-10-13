# dashboard/views.py

from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

def index(request):
    """Home page - TAMPILKAN FRONTEND"""
    return render(request, 'dashboard/index.html')  # ✅ PERBAIKAN DI SINI

@csrf_protect
def custom_logout(request):
    """Custom logout yang pasti bekerja"""
    logout(request)
    return redirect('login')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
