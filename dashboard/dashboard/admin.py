from django.contrib import admin
from django.utils.html import format_html
from .models import Dast
from .models import Sast

class DastAdmin(admin.ModelAdmin):
    list_display = ('nama_website_link', 'link')

    def nama_website_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.nama_website)

    nama_website_link.short_description = "Nama Website"

    def link_tautan(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)
    link_tautan.short_description = "Link"

class SastAdmin(admin.ModelAdmin):
    list_display = ('nama_aplikasi', 'versi_aplikasi', 'tanggal_scan', 'link_hasil_scan_display')

    def link_hasil_scan_display(self, obj):
        if obj.link_hasil_scan:
           return format_html('<a href="{}" target="_blank">Lihat Hasil Scan</a>', obj.link_hasil_scan)
        return "-"
    link_hasil_scan_display.short_descriptiuon = " Hasil Scan"

admin.site.register(Dast, DastAdmin)
admin.site.register(Sast, SastAdmin)
#admin.site.register(ReportSast, ReportSastAdmin)
