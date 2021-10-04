from django.contrib import admin
from .models import Pelatihan, Rekomendasi

# class RekomendasiInline(admin.TabularInline):
#     model = Rekomendasi
#     fk_name = "to_pelatihan"

# class RekomendasiPelatihan(admin.ModelAdmin):
#     inlines = [
#         RekomendasiInline,
#     ]

# Register your models here.
admin.site.register(Pelatihan)
admin.site.register(Rekomendasi)