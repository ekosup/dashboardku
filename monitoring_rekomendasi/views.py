from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.db.models import Avg

import wordcloud as wc

from .models import Pelatihan, Rekomendasi

class CustomLoginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("monitoring:home")

def word_count(str):
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def home(request):
    pelatihan = Pelatihan.objects.all()
    avg_rating = pelatihan.aggregate(Avg('rating_pelatihan'))
    jum_pelatihan = pelatihan.count()

    sorted_pelatihan = pelatihan.order_by('rating_pelatihan')[:5]
    picked_pelatihan = []
    for i in sorted_pelatihan:
        temp = {}
        temp['nama'] = i.nama_pelatihan
        temp['rating'] = i.rating_pelatihan
        temp['ratio'] = (i.rating_pelatihan / 5) * 100
        picked_pelatihan.append(temp)

    # Get recommendation object
    rekomendasi = Rekomendasi.objects.filter(diselesaikan=False).count()

    # Get summ of ratings
    avg_rating = round(avg_rating['rating_pelatihan__avg'],2)
    percentage_rating = round(avg_rating/5 * 100, 2)

    test = Rekomendasi.objects.values_list('deskripsi', flat=True)
    test = " ".join(list(test)).lower()
    test = word_count(test)
    words = []
    for k, v in test.items():
        temp = {}
        temp["word"] = k
        temp["size"] = v * 15
        words.append(temp)
    # print(words)

    ## Pass context to template
    context = {
        'pelatihan' : picked_pelatihan,
        'jum_pelatihan' : jum_pelatihan,
        'avg_rating' : avg_rating,
        'avg_rating_percent' : percentage_rating,
        'need_attention': rekomendasi,
        'words': words,
    }

    return render(request, 'main.html', context)

class PelatihanList(LoginRequiredMixin, ListView):
    model = Pelatihan
    context_object_name = "pelatihan"
    template_name = 'daftar_pelatihan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ## Search feature
        # context['pelatihan'] = context['pelatihan'].filter(user=self.request.user)
        # context['count_incomplete'] = context['tasks'].filter(complete=False).count()

        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__icontains=search_input)
        
        # context['search_input'] = search_input

        return context

class PelatihanCreate(LoginRequiredMixin, CreateView):
    model = Pelatihan
    fields = "__all__"
    context_object_name = "pelatihan"
    template_name = "form_pelatihan.html"
    success_url = reverse_lazy('monitoring:pelatihan')

class PelatihanUpdate(LoginRequiredMixin, UpdateView):
    model = Pelatihan
    fields = "__all__"
    success_url = reverse_lazy('monitoring:pelatihan')
    template_name = "form_pelatihan.html"

class RekomendasiPelatihan(ListView):
    model = Rekomendasi
    context_object_name = 'rekomendasi'
    template_name = 'daftar_rekomendasi.html'
