from django.db import models

class Dast(models.Model):
    link = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True) 
    nama_website = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_website



class Sast(models.Model):
    nama_aplikasi = models.CharField(max_length=255)
    versi_aplikasi = models.CharField(max_length=50)
    hasil_scan = models.TextField()
    tanggal_scan = models.DateTimeField(auto_now_add=True)
    link_hasil_scan = models.TextField()

    def __str__(self):
        return self.nama_aplikasi
