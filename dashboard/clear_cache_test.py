import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.core.cache import cache
from django.contrib.sessions.models import Session

def clear_cache_and_sessions():
    print("🗑️  CLEARING CACHE & SESSIONS")
    print("=" * 50)
    
    # Clear cache
    try:
        cache.clear()
        print("✅ Cache cleared")
    except:
        print("❌ Cache clear failed")
    
    # Count sessions
    session_count = Session.objects.count()
    print(f"📊 Active sessions: {session_count}")
    
    print("\n💡 TROUBLESHOOTING STEPS:")
    print("   1. Clear browser cache: Ctrl+Shift+R (Hard reload)")
    print("   2. Try incognito/private window")
    print("   3. Check browser console for errors (F12)")
    print("   4. Try different browser")

if __name__ == '__main__':
    clear_cache_and_sessions()
