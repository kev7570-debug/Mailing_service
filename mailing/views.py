from django.shortcuts import render
from .models import Mailing, Client

def home(request):
    context = {
        'total_mailings': Mailing.objects.count(),
        'active_mailings': Mailing.objects.filter(status='Запущена').count(),
        'unique_clients': Client.objects.count(),
    }
    return render(request, 'mailing/home.html', context)
