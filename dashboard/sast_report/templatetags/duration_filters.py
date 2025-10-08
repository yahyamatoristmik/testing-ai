from django import template
import datetime

register = template.Library()

@register.filter
def duration_display(value):
    """Safe duration display filter for templates"""
    if not value:
        return "N/A"
    
    try:
        # Handle jika value adalah timedelta
        if hasattr(value, 'total_seconds'):
            total_seconds = int(value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return "N/A"
    except:
        return "N/A"
