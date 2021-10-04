from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import PelatihanUpdate, home, CustomLoginView, PelatihanList, PelatihanCreate, RekomendasiPelatihan

app_name = 'monitoring'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='monitoring:home'), name='logout'),

    path('', home, name='home'),
    path('pelatihan/', PelatihanList.as_view(), name='pelatihan'),
    path('pelatihan/create/', PelatihanCreate.as_view(), name='create-pelatihan'),
    path('pelatihan/update/<int:pk>/', PelatihanUpdate.as_view(), name='update-pelatihan'),
    
    path('rekomendasi/', RekomendasiPelatihan.as_view(), name='rekomendasi'),

]