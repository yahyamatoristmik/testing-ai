# ==========================================
# message/models.py
# ==========================================
from django.db import models

class Message(models.Model):
    # Basic contact information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200)
    
    # Service field dengan choices
    SERVICE_CHOICES = [
	('VAPT', 'VAPT (Vulnerability Assemnt & Penetration'),
        ('RedTeam', 'Red Teaming Expert'),
        ('SAST', 'SAST (Static Applicatiuon Security Testing)'),
        ('DAST', 'DAST (Dynamic Application Security Testing)'),
	('SOC', '24/7 Security Operation'),
	('Monitoring', 'Monitoring & Incident Response'),
        ('Consulting', 'Cybersecurity Consulting'),
	('Security Awarenes','Security Awarenes'),
        ('Breach Investigasi', 'Breach Investigasi'),
	('DarkWeb', 'DarkWeb Monitoring'),
	('other', 'Other'),
    ]
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, null=True)
    
    # Message content
    message = models.TextField()
    
    # Status tracking
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    
    # Priority
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['priority', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"
