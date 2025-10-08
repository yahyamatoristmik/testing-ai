# ==========================================
# message/admin.py
# ==========================================
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'service', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'service', 'created_at']
    search_fields = ['name', 'email', 'subject', 'company']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'priority']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('subject', 'service', 'message')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
