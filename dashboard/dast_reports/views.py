from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import DASTScan
import json
import os
import requests
from django.conf import settings
from django.utils import timezone
import secrets
import logging
import re
import time
# ✅ DEFINISIKAN LOGGER
logger = logging.getLogger(__name__)

# ==================== FUNGSI EXISTING ====================

@staff_member_required
def scan_report_view(request, scan_id):
    """
    View untuk menampilkan report detail dari scan
    """
    scan = get_object_or_404(DASTScan, id=scan_id)
    
    # PERIKSA PERMISSION
    if not request.user.is_superuser and scan.owner != request.user:
        return HttpResponseRedirect(reverse('admin:index'))

    # Cari path JSON report
    json_report_path = None
    if scan.json_report_path and os.path.exists(scan.json_report_path):
        json_report_path = scan.json_report_path
    elif scan.jenkins_build_number:
        json_report_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.jenkins_build_number}.json"
    else:
        json_report_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.id}.json"

    # Parse JSON report
    report_data = None
    if os.path.exists(json_report_path):
        try:
            with open(json_report_path, 'r') as f:
                report_data = json.load(f)
        except Exception as e:
            report_data = {"error": f"Gagal memparse JSON: {str(e)}"}
    else:
        report_data = {"error": f"File report tidak ditemukan: {json_report_path}"}

    context = {
        'scan': scan,
        'report_data': report_data,
        'title': f'Report for {scan.name}',
    }

    return render(request, 'admin/dast_reports/report.html', context)

@csrf_exempt
@staff_member_required
def trigger_zap_scan_view(request, scan_id):
    """View untuk trigger single scan dari button"""
    try:
        scan = DASTScan.objects.get(id=scan_id)
        # Di sini nanti akan panggil Jenkins trigger
        return JsonResponse({
            'status': 'success', 
            'message': f'Scan triggered for {scan.target_url}'
        })
    except DASTScan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Scan not found'})

# ==================== FUNGSI BARU AI RECOMMENDATIONS ====================
@staff_member_required
def ai_recommendations_view(request, object_id):
    """View untuk menampilkan AI recommendations"""
    scan = get_object_or_404(DASTScan, id=object_id)
    
    # Permission check
    if not request.user.is_superuser and scan.owner != request.user:
        return HttpResponseRedirect(reverse('admin:index'))
    
    context = {
        'scan': scan,
        'title': f'AI Recommendations - {scan.name}',
    }
    
    return render(request, 'admin/dast_reports/ai_recommendations.html', context)

@staff_member_required
@csrf_exempt
def generate_ai_recommendations(request, scan_id):
    """
    Generate AI recommendations - SIMPLE WORKING VERSION
    """
    print(f"🚀 START AI Generation for scan {scan_id}")
    start_time = time.time()  # ✅ SEKARANG HARUSNYA WORK
    
    try:
        scan = get_object_or_404(DASTScan, id=scan_id)
        
        # Permission check
        if not request.user.is_superuser and scan.owner != request.user:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'})
        
        if scan.status != 'completed':
            return JsonResponse({'status': 'error', 'message': 'Scan must be completed'})
        
        # Update status to processing
        scan.ai_analysis_status = 'processing'
        scan.save(update_fields=['ai_analysis_status'])
        
        print(f"📊 Scan: {scan.name}, URL: {scan.target_url}")
        
        # 1. CARI JSON REPORT FILE
        json_report_path = None
        possible_paths = [
            scan.json_report_path,
            f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.jenkins_build_number}.json",
            f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.id}.json",
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                json_report_path = path
                break
        
        if not json_report_path:
            error_msg = "Report file not found"
            print(f"❌ {error_msg}")
            return create_fallback_response(request, scan, [], error_msg)
        
        print(f"📁 Found report: {json_report_path}")
        
        # 2. BACA JSON REPORT
        with open(json_report_path, 'r') as f:
            report_data = json.load(f)
        
        alerts = report_data.get('site', [{}])[0].get('alerts', [])
        print(f"🔍 Found {len(alerts)} alerts")
        
        # 3. BUAT PROMPT SEDERHANA DULU
        prompt = create_simple_prompt(scan, alerts)
        
        # 4. CALL OPENROUTER API
        api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
        if not api_key:
            print("❌ API key not found")
            return create_fallback_response(request, scan, alerts, "API key missing")
        
        print("🌐 Calling OpenRouter API...")
        
        recommendations = call_openrouter_api_simple(api_key, prompt)
        
        # 5. SIMPAN HASIL
        scan.ai_recommendations = recommendations
        scan.ai_analysis_status = 'completed'
        scan.ai_analysis_date = timezone.now()
        
        if not scan.report_token:
            scan.report_token = secrets.token_urlsafe(32)
            
        scan.save()
        
        elapsed_time = time.time() - start_time
        print(f"✅ AI Generation COMPLETED in {elapsed_time:.1f} seconds")
        
        # 6. RETURN RESPONSE
        return JsonResponse({
            'status': 'success', 
            'message': f'AI recommendations generated in {elapsed_time:.1f}s',
            'redirect_url': reverse('admin:dastscan_ai_recommendations', args=[scan.id])
        })
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"💥 ERROR after {elapsed_time:.1f}s: {str(e)}")
        traceback.print_exc()
        
        return JsonResponse({
            'status': 'error', 
            'message': f'Error: {str(e)}'
        }, status=500)

def create_simple_prompt(scan, alerts):
    """Buat prompt sederhana yang work"""
    
    prompt = f"""
Berdasarkan scan keamanan OWASP ZAP untuk website {scan.target_url} yang menemukan {len(alerts)} vulnerability, berikan rekomendasi perbaikan keamanan dalam format JSON:

{{
  "summary": {{
    "target_url": "{scan.target_url}",
    "total_vulnerabilities": {len(alerts)},
    "overall_risk": "high/medium/low"
  }},
  "recommendations": [
    {{
      "priority": "high/medium/low",
      "title": "Judul rekomendasi",
      "description": "Deskripsi rekomendasi",
      "action": "Tindakan yang perlu dilakukan"
    }}
  ]
}}
"""
    return prompt

def call_openrouter_api_simple(api_key, prompt):
    """API call sederhana"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            
            # Cleanup response
            if '```json' in ai_content:
                ai_content = ai_content.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_content:
                ai_content = ai_content.split('```')[1].split('```')[0].strip()
            
            return json.loads(ai_content)
        else:
            print(f"❌ API error {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ API call error: {e}")
        return None

def create_fallback_response(request, scan, alerts, reason):
    """Fallback response"""
    
    fallback = {
        "summary": {
            "target_url": scan.target_url,
            "total_vulnerabilities": len(alerts),
            "overall_risk": "high" if len(alerts) > 0 else "low",
            "fallback_reason": reason
        },
        "recommendations": [
            {
                "priority": "high",
                "title": "Security Review Required",
                "description": "Lakukan review keamanan menyeluruh berdasarkan temuan OWASP ZAP",
                "action": "Consult with security team untuk analisis lebih lanjut"
            }
        ]
    }
    
    scan.ai_recommendations = fallback
    scan.ai_analysis_status = 'completed'
    scan.ai_analysis_date = timezone.now()
    
    if not scan.report_token:
        scan.report_token = secrets.token_urlsafe(32)
        
    scan.save()
    
    return JsonResponse({
        'status': 'success', 
        'message': f'Fallback recommendations generated ({reason})',
        'redirect_url': reverse('admin:dastscan_ai_recommendations', args=[scan.id])
    })

@login_required
def public_ai_report_view(request, scan_id, token):
    """
    View publik untuk melihat laporan AI dengan token
    """
    scan = get_object_or_404(DASTScan, id=scan_id)
    
    # Check token
    if scan.report_token != token:
        return HttpResponseForbidden("Token tidak valid")
    
    context = {
        'scan': scan,
        'title': f'Laporan Keamanan - {scan.name}',
        'is_public': True,
    }
    
    return render(request, 'admin/dast_reports/public_ai_report.html', context)

@login_required
def check_running_scans(request):
    """API untuk check jika ada scan yang masih running"""
    from .models import DASTScan
    
    if request.user.is_superuser:
        running_scans = DASTScan.objects.filter(status__in=['running', 'pending']).exists()
    else:
        running_scans = DASTScan.objects.filter(
            owner=request.user, 
            status__in=['running', 'pending']
        ).exists()
    
    return JsonResponse({
        'has_running_scans': running_scans,
        'timestamp': timezone.now().isoformat()
    })

@staff_member_required
def test_view(request):
    """Test view untuk debug"""
    return JsonResponse({
        'status': 'success',
        'message': 'Test view works!',
        'user': request.user.username,
        'is_authenticated': request.user.is_authenticated,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser
    })
