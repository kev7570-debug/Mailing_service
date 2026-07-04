from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Count
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .services import send_mailing


# Главная страница со статистикой
def home(request):
    context = {
        'total_mailings': Mailing.objects.count(),
        'active_mailings': Mailing.objects.filter(status='Запущена').count(),
        'unique_clients': Client.objects.count(),
        'total_attempts': MailingAttempt.objects.count(),
        'successful_attempts': MailingAttempt.objects.filter(status='Успешно').count(),
    }
    return render(request, 'mailing/home.html', context)


# ==================== CRUD для клиентов ====================

class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'
    ordering = ['full_name']


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент "%(full_name)s" успешно добавлен!'


class ClientUpdateView(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент "%(full_name)s" успешно обновлён!'


class ClientDeleteView(SuccessMessageMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент успешно удалён!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для сообщений ====================

class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    ordering = ['-id']


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(SuccessMessageMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение "%(subject)s" успешно создано!'


class MessageUpdateView(SuccessMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение "%(subject)s" успешно обновлено!'


class MessageDeleteView(SuccessMessageMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение успешно удалено!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для рассылок ====================

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    ordering = ['-start_time']


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← Обновляем статус при каждом просмотре
        return obj


class MailingCreateView(SuccessMessageMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно создана!'


class MailingUpdateView(SuccessMessageMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно обновлена!'


class MailingDeleteView(SuccessMessageMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно удалена!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== Ручной запуск рассылки ====================

def send_mailing_view(request, pk):
    """Представление для ручного запуска рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)

    # Запускаем отправку
    send_mailing(pk)

    # Показываем сообщение об успехе
    messages.success(request, f'Рассылка #{pk} успешно запущена!')

    # Возвращаемся на страницу деталей рассылки
    return redirect('mailing:mailing_detail', pk=pk)
