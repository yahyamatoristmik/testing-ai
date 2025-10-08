from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DASTScan(models.Model):
    """
    Model untuk menyimpan data DAST (Dynamic Application Security Testing) scan.
    Setiap scan memiliki pemilik (owner) yang hanya bisa melihat scan miliknya sendiri.
    """
    
    # Status choices
    SCAN_STATUS = [
        ('pending', '🟡 Pending'),
        ('running', '🟠 Running'),
        ('completed', '🟢 Completed'),
        ('failed', '🔴 Failed'),
        ('canceled', '⚫ Canceled'),
    ]
    
    # Scan type choices
    SCAN_TYPE = [
        ('full', 'Full Scan'),
        ('quick', 'Quick Scan'),
        ('api', 'API Scan'),
        ('crawl', 'Crawl Only'),
    ]

    # ==================== BASIC INFORMATION ====================
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dast_scans',
        verbose_name="Pemilik Scan",
        null=True,
        blank=True
    )
    
    name = models.CharField(
        max_length=200, 
        default="DAST Scan",
        verbose_name="Nama Scan"
    )
    
    target_url = models.URLField(
        max_length=500, 
        verbose_name="Target URL"
    )
    
    scan_type = models.CharField(
        max_length=20, 
        choices=SCAN_TYPE, 
        default='full',
        verbose_name="Tipe Scan"
    )

    # ==================== SCAN DETAILS ====================
    scan_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Tanggal Scan"
    )
    
    completed_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Tanggal Selesai"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=SCAN_STATUS, 
        default='pending',
        verbose_name="Status"
    )

    # ==================== RESULTS ====================
    results = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name="Hasil Scan"
    )
    
    vulnerabilities_found = models.IntegerField(
        default=0, 
        verbose_name="Total Vulnerabilitas"
    )
    
    high_vulnerabilities = models.IntegerField(
        default=0, 
        verbose_name="Risiko Tinggi"
    )
    
    medium_vulnerabilities = models.IntegerField(
        default=0, 
        verbose_name="Risiko Sedang"
    )
    
    low_vulnerabilities = models.IntegerField(
        default=0, 
        verbose_name="Risiko Rendah"
    )
    
    informational_vulnerabilities = models.IntegerField(
        default=0, 
        verbose_name="Informasional"
    )

    # ==================== PERFORMANCE METRICS ====================
    scan_duration = models.DurationField(
        null=True, 
        blank=True, 
        verbose_name="Durasi Scan"
    )
    
    pages_crawled = models.IntegerField(
        default=0, 
        verbose_name="Halaman Di-crawl"
    )
    
    requests_made = models.IntegerField(
        default=0, 
        verbose_name="Request Dibuat"
    )

    # ==================== CONFIGURATION ====================
    scan_config = models.JSONField(
        default=dict, 
        blank=True, 
        null=True, 
        verbose_name="Konfigurasi Scan"
    )
    
    active = models.BooleanField(
        default=True, 
        verbose_name="Scan Aktif"
    )
    
    scheduled = models.BooleanField(
        default=False, 
        verbose_name="Scan Terjadwal"
    )

    # ==================== JENKINS INTEGRATION ====================
    jenkins_build_number = models.IntegerField(
        null=True, 
        blank=True, 
        unique=True,
        verbose_name="Nomor Build Jenkins"
    )
    
    json_report_path = models.CharField(
        max_length=500, 
        blank=True,
        null=True,
        verbose_name="Path Laporan JSON"
    )

    # ==================== METADATA ====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Dibuat Pada"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Diupdate Pada"
    )

    # ==================== AI RECOMMENDATIONS ====================
    ai_recommendations = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name="Rekomendasi AI",
        help_text="Rekomendasi keamanan yang dihasilkan oleh AI"
    )

    ai_analysis_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '🟡 Menunggu Analisis'),
            ('processing', '🟠 Sedang Dianalisis'),
            ('completed', '🟢 Analisis Selesai'),
            ('failed', '🔴 Analisis Gagal'),
        ],
        default='pending',
        verbose_name="Status Analisis AI"
    )

    ai_analysis_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Tanggal Analisis AI"
    )

    report_token = models.CharField(
        max_length=100, 
        blank=True,
        default='',
        verbose_name="Token Laporan",
        help_text="Token untuk akses aman ke laporan AI"
    )

    class Meta:
        verbose_name = "DAST Scan"
        verbose_name_plural = "DAST Scans"
        ordering = ['-scan_date']
        permissions = [
            ("view_own_dastscan", "Can view own DAST scans only"),
            ("view_all_dastscan", "Can view all DAST scans"),
        ]

    def __str__(self):
        """String representation of the model"""
        owner_name = self.owner.username if self.owner else "System"
        return f"{self.name} - {self.target_url} ({owner_name})"

    def save(self, *args, **kwargs):
        """
        Custom save method untuk:
        1. Auto-calculate vulnerabilities
        2. Normalize URL
        3. Auto-set scan_config
        4. Auto-set owner dari request
        """
        # 1. Hitung total vulnerabilities
        self.calculate_vulnerabilities()
        
        # 2. Normalize URL (remove trailing slash)
        self.normalize_url()
        
        # 3. Auto-set scan_config jika kosong
        self.auto_set_scan_config()
        
        # 4. Auto-set owner dari request jika available
        self.auto_set_owner()
        
        super().save(*args, **kwargs)

    def calculate_vulnerabilities(self):
        """Hitung total vulnerabilities"""
        self.vulnerabilities_found = (
            self.high_vulnerabilities + 
            self.medium_vulnerabilities + 
            self.low_vulnerabilities + 
            self.informational_vulnerabilities
        )

    def normalize_url(self):
        """Normalize URL dengan remove trailing slash dan konsisten format"""
        if self.target_url:
            # Remove trailing slash dan convert to lowercase untuk konsistensi
            parsed = urlparse(self.target_url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
            self.target_url = normalized_url

    def auto_set_scan_config(self):
        """Auto-set scan_config dari settings jika kosong"""
        if not self.scan_config or self.scan_config == {}:
            jenkins_config = getattr(settings, 'JENKINS_CONFIG', {})
            self.scan_config = {
                "jenkins": {
                    "base_url": jenkins_config.get('BASE_URL', ''),
                    "username": jenkins_config.get('USERNAME', ''),
                    "api_token": jenkins_config.get('API_TOKEN', ''),
                    "job_name": jenkins_config.get('ZAP_JOB_NAME', ''),
                    "job_token": jenkins_config.get('ZAP_JOB_TOKEN', '')
                },
                "scan_parameters": {
                    "target_url": self.target_url,
                    "scan_type": self.scan_type,
                    "auto_configured": True,
                    "configured_at": timezone.now().isoformat()
                }
            }

    def auto_set_owner(self):
        """Auto-set owner dari request jika available"""
        if not self.owner_id and hasattr(self, '_request'):
            self.owner = self._request.user

    # ==================== PROPERTIES ====================
    @property
    def duration_formatted(self):
        """Format duration menjadi readable string"""
        if self.scan_duration:
            total_seconds = int(self.scan_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return "N/A"

    @property
    def risk_score(self):
        """Hitung risk score berdasarkan bobot vulnerabilities"""
        return (
            self.high_vulnerabilities * 10 + 
            self.medium_vulnerabilities * 5 + 
            self.low_vulnerabilities * 2 + 
            self.informational_vulnerabilities * 1
        )

    @property
    def risk_level(self):
        """Tentukan level risk berdasarkan score"""
        score = self.risk_score
        if score >= 50:
            return "high"
        elif score >= 20:
            return "medium"
        elif score >= 10:
            return "low"
        else:
            return "info"

    # ==================== METHODS ====================
    def get_existing_scan_data(self):
        """
        Mendapatkan data dari scan yang sudah completed untuk URL yang sama.
        Berguna untuk pre-fill data saat scan ulang.
        """
        existing_scan = DASTScan.objects.filter(
            target_url=self.target_url,
            status='completed'
        ).exclude(id=self.id).order_by('-completed_date').first()
        
        if existing_scan:
            return {
                'high_vulnerabilities': existing_scan.high_vulnerabilities,
                'medium_vulnerabilities': existing_scan.medium_vulnerabilities,
                'low_vulnerabilities': existing_scan.low_vulnerabilities,
                'informational_vulnerabilities': existing_scan.informational_vulnerabilities,
                'vulnerabilities_found': existing_scan.vulnerabilities_found,
                'scan_duration': existing_scan.scan_duration,
                'json_report_path': existing_scan.json_report_path
            }
        return None

    def check_jenkins_status(self):
        """
        Mengecek status build Jenkins dan update status scan accordingly.
        Return: True jika status berubah, False jika tidak.
        """
        if not self.jenkins_build_number or self.status not in ['running', 'pending']:
            return False
        
        try:
            jenkins_config = getattr(settings, 'JENKINS_CONFIG', {})
            base_url = jenkins_config.get('BASE_URL')
            username = jenkins_config.get('USERNAME')
            api_token = jenkins_config.get('API_TOKEN')
            job_name = jenkins_config.get('ZAP_JOB_NAME', 'DAST-Automasi')
            
            if not all([base_url, username, api_token]):
                return False
            
            # Build Jenkins API URL
            jenkins_url = f"{base_url.rstrip('/')}/job/{job_name}/{self.jenkins_build_number}/api/json"
            
            # Request ke Jenkins API
            response = requests.get(
                jenkins_url,
                auth=(username, api_token),
                timeout=10
            )
            
            if response.status_code == 200:
                build_info = response.json()
                
                # Pastikan build sudah selesai
                if build_info.get('building', True) == False:
                    if build_info.get('result') == 'SUCCESS':
                        DASTScan.objects.filter(id=self.id).update(
                            status='completed',
                            completed_date=timezone.now()
                        )
                        logger.info(f"Scan {self.id} updated to completed")
                        return True
                        
                    elif build_info.get('result') in ['FAILURE', 'ABORTED', 'UNSTABLE']:
                        DASTScan.objects.filter(id=self.id).update(
                            status='failed', 
                            completed_date=timezone.now()
                        )
                        logger.info(f"Scan {self.id} updated to failed")
                        return True
            
            elif response.status_code == 404:
                logger.warning(f"Jenkins build {self.jenkins_build_number} not found for scan {self.id}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking Jenkins status for build {self.jenkins_build_number}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error checking Jenkins status: {str(e)}")
        
        return False

    def is_owned_by(self, user):
        """Check jika scan dimiliki oleh user tertentu"""
        return self.owner == user

    def can_view(self, user):
        """Check jika user bisa melihat scan ini"""
        return user.is_superuser or self.owner == user

    def can_edit(self, user):
        """Check jika user bisa edit scan ini"""
        return user.is_superuser or self.owner == user

    def can_delete(self, user):
        """Check jika user bisa delete scan ini"""
        return user.is_superuser or self.owner == user

    # ==================== CLASS METHODS ====================
    @classmethod
    def update_completed_scans(cls):
        """
        Method untuk update semua scan yang running dan build number-nya sudah complete di Jenkins.
        """
        from django.db import transaction
        
        running_scans = cls.objects.filter(status='running', jenkins_build_number__isnull=False)
        updated_count = 0
        
        for scan in running_scans:
            try:
                with transaction.atomic():
                    # Gunakan select_for_update untuk lock row
                    fresh_scan = cls.objects.select_for_update().get(id=scan.id)
                    
                    # Pastikan masih running sebelum update
                    if fresh_scan.status == 'running':
                        if fresh_scan.check_jenkins_status():
                            updated_count += 1
                            
            except Exception as e:
                logger.error(f"Error updating scan {scan.id}: {str(e)}")
                continue
        
        return updated_count

    @classmethod
    def get_user_scans(cls, user):
        """Get semua scans untuk user tertentu"""
        if user.is_superuser:
            return cls.objects.all()
        return cls.objects.filter(owner=user)

    @classmethod
    def get_running_scans(cls, user=None):
        """Get running scans, optionally filtered by user"""
        queryset = cls.objects.filter(status='running')
        if user and not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset

    @classmethod
    def get_completed_scans(cls, user=None):
        """Get completed scans, optionally filtered by user"""
        queryset = cls.objects.filter(status='completed')
        if user and not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset

    @classmethod
    def create_scan(cls, target_url, scan_name, scan_type='full', owner=None):
        """
        Helper method untuk membuat scan baru dengan validation.
        """
        # Normalize URL
        parsed = urlparse(target_url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
        
        # Cek jika sudah ada running scan untuk URL yang sama
        existing_running = cls.objects.filter(
            target_url=normalized_url,
            status='running'
        )
        
        if existing_running.exists():
            raise ValueError(f"Sudah ada scan yang berjalan untuk {normalized_url}")
        
        # Buat scan baru
        scan = cls(
            target_url=normalized_url,
            name=scan_name or f"Scan {normalized_url}",
            scan_type=scan_type,
            owner=owner
        )
        
        scan.save()
        return scan

    def generate_ai_recommendations(self):
        """
        Generate AI recommendations for the scan results
        """
        from django.conf import settings
        import requests
        import json
        
        if not self.results or self.ai_analysis_status == 'processing':
            return False
        
        try:
            # Update status to processing
            self.ai_analysis_status = 'processing'
            self.save()
            
            # Prepare data for AI analysis
            alerts = self.results.get('site', [{}])[0].get('alerts', [])
            
            # Create prompt for AI
            prompt = f"""
            Saya memiliki laporan keamanan DAST dari OWASP ZAP untuk website {self.target_url}. 
            Berikut adalah daftar vulnerability yang ditemukan:
            
            {json.dumps(alerts, indent=2)}

            Berikan rekomendasi perbaikan keamanan yang spesifik dalam bahasa Indonesia untuk setiap vulnerability.
            Kelompokkan berdasarkan tingkat keparahan (High, Medium, Low).
            Untuk setiap rekomendasi, sertakan contoh implementasi yang konkret kode sebelum dan sesudah perbaikan.
            Format output harus JSON dengan struktur:
            {{
              "summary": {{
                "total_vulnerabilities": 0,
                "risk_score": 0,
                "overall_risk": "string"
              }},
              "recommendations": [
                {{
                  "pluginid": "string",
                  "alert": "string",
                  "risk_level": "high|medium|low|info",
                  "description": "string",
                  "recommendation": "string",
                  "implementation_example": "string"
                }}
              ]
            }}
            """
            
            # Call DeepSeek API
            headers = {
                "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Parse AI response (remove markdown code blocks if present)
                if '```json' in ai_response:
                    ai_response = ai_response.split('```json')[1].split('```')[0].strip()
                elif '```' in ai_response:
                    ai_response = ai_response.split('```')[1].split('```')[0].strip()
                
                # Parse JSON response
                recommendations = json.loads(ai_response)
                
                # Save recommendations
                self.ai_recommendations = recommendations
                self.ai_analysis_status = 'completed'
                self.ai_analysis_date = timezone.now()
                
                # Generate secure token if not exists
                if not self.report_token:
                    import secrets
                    self.report_token = secrets.token_urlsafe(32)
                    
                self.save()
                return True
                
            else:
                self.ai_analysis_status = 'failed'
                self.save()
                return False
                
        except Exception as e:
            logger.error(f"Error generating AI recommendations for scan {self.id}: {str(e)}")
            self.ai_analysis_status = 'failed'
            self.save()
            return False

    def get_ai_recommendations_url(self):
        """Generate URL untuk melihat rekomendasi AI"""
        from django.urls import reverse
        if self.report_token:
            return reverse('dastscan_ai_report', kwargs={'scan_id': self.id, 'token': self.report_token})
        return None
