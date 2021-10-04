from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.
class Pelatihan(models.Model):
    nama_pelatihan = models.CharField(max_length=200)
    tanggal_mulai = models.DateField(null=True)
    tanggal_selesai = models.DateField(null=True)
    pic_pelatihan = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_pelatihan = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nama_pelatihan}"

class Rekomendasi(models.Model):
    choices = [('RB', 'Renbang'), ('EV', 'Evalap'), ('TU', 'TU'), ('PY', 'Penyelenggaraan')]
    deadline = timezone.now() + timezone.timedelta(7,0,0)

    nama_pelatihan = models.ForeignKey(Pelatihan, on_delete=models.CASCADE)
    deskripsi = models.TextField(null=True)
    penanggung_jawab = models.CharField(max_length=2, choices=choices, default='TU')
    diselesaikan = models.BooleanField(default=False)
    target_penyelesaian = models.DateField(default=deadline)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nama_pelatihan} - {self.penanggung_jawab}"
    
