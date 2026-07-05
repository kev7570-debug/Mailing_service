# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse_lazy
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib import messages
# from django.db.models import Count
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import login
# from .models import Client, Message, Mailing, MailingAttempt
# from .forms import ClientForm, MessageForm, MailingForm, CustomUserCreationForm
# from .services import send_mailing
#
#
# # Главная страница со статистикой
# def home(request):
#     context = {
#         'total_mailings': Mailing.objects.count(),
#         'active_mailings': Mailing.objects.filter(status='Запущена').count(),
#         'unique_clients': Client.objects.count(),
#         'total_attempts': MailingAttempt.objects.count(),
#         'successful_attempts': MailingAttempt.objects.filter(status='Успешно').count(),
#     }
#     return render(request, 'mailing/home.html', context)
#
#
# # ==================== CRUD для клиентов ====================
#
# class ClientListView(LoginRequiredMixin, ListView):
#     model = Client
#     template_name = 'mailing/client_list.html'
#     context_object_name = 'clients'
#     ordering = ['full_name']
#
#     def get_queryset(self):
#         return Client.objects.filter(owner=self.request.user)
#
#
# class ClientDetailView(LoginRequiredMixin, DetailView):
#     model = Client
#     template_name = 'mailing/client_detail.html'
#     context_object_name = 'client'
#
#     def get_queryset(self):
#         return Client.objects.filter(owner=self.request.user)
#
#
# class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Client
#     form_class = ClientForm
#     template_name = 'mailing/client_form.html'
#     success_url = reverse_lazy('mailing:client_list')
#     success_message = 'Клиент "%(full_name)s" успешно добавлен!'
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)
#
#
# class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Client
#     form_class = ClientForm
#     template_name = 'mailing/client_form.html'
#     success_url = reverse_lazy('mailing:client_list')
#     success_message = 'Клиент "%(full_name)s" успешно обновлён!'
#
#
# class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Client
#     template_name = 'mailing/client_confirm_delete.html'
#     success_url = reverse_lazy('mailing:client_list')
#     success_message = 'Клиент успешно удалён!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # ==================== CRUD для сообщений ====================
#
# class MessageListView(LoginRequiredMixin, ListView):
#     model = Message
#     template_name = 'mailing/message_list.html'
#     context_object_name = 'messages'
#     ordering = ['-id']
#
#     def get_queryset(self):
#         return Message.objects.filter(owner=self.request.user)
#
#
# class MessageDetailView(LoginRequiredMixin, DetailView):
#     model = Message
#     template_name = 'mailing/message_detail.html'
#     context_object_name = 'message'
#
#     def get_queryset(self):
#         return Message.objects.filter(owner=self.request.user)
#
#
# class MessageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Message
#     form_class = MessageForm
#     template_name = 'mailing/message_form.html'
#     success_url = reverse_lazy('mailing:message_list')
#     success_message = 'Сообщение "%(subject)s" успешно создано!'
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)
#
#
# class MessageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Message
#     form_class = MessageForm
#     template_name = 'mailing/message_form.html'
#     success_url = reverse_lazy('mailing:message_list')
#     success_message = 'Сообщение "%(subject)s" успешно обновлено!'
#
#
# class MessageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Message
#     template_name = 'mailing/message_confirm_delete.html'
#     success_url = reverse_lazy('mailing:message_list')
#     success_message = 'Сообщение успешно удалено!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # ==================== CRUD для рассылок ====================
#
# class MailingListView(LoginRequiredMixin, ListView):
#     model = Mailing
#     template_name = 'mailing/mailing_list.html'
#     context_object_name = 'mailings'
#     ordering = ['-start_time']
#
#     def get_queryset(self):
#         return Mailing.objects.filter(owner=self.request.user)
#
#
# class MailingDetailView(LoginRequiredMixin, DetailView):
#     model = Mailing
#     template_name = 'mailing/mailing_detail.html'
#     context_object_name = 'mailing'
#
#     def get_queryset(self):
#         return Mailing.objects.filter(owner=self.request.user)
#
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         obj.update_status()
#         return obj
#
#
# class MailingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Mailing
#     form_class = MailingForm
#     template_name = 'mailing/mailing_form.html'
#     success_url = reverse_lazy('mailing:mailing_list')
#     success_message = 'Рассылка успешно создана!'
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)
#
#
# class MailingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Mailing
#     form_class = MailingForm
#     template_name = 'mailing/mailing_form.html'
#     success_url = reverse_lazy('mailing:mailing_list')
#     success_message = 'Рассылка успешно обновлена!'
#
#
# class MailingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = Mailing
#     template_name = 'mailing/mailing_confirm_delete.html'
#     success_url = reverse_lazy('mailing:mailing_list')
#     success_message = 'Рассылка успешно удалена!'
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)
#
#
# # ==================== Ручной запуск рассылки ====================
#
# def send_mailing_view(request, pk):
#     """Представление для ручного запуска рассылки"""
#     mailing = get_object_or_404(Mailing, pk=pk)
#
#     # Проверяем, что пользователь является владельцем рассылки
#     if mailing.owner != request.user:
#         messages.error(request, 'У вас нет прав для запуска этой рассылки.')
#         return redirect('mailing:mailing_list')
#
#     # Запускаем отправку
#     send_mailing(pk)
#
#     # Показываем сообщение об успехе
#     messages.success(request, f'Рассылка #{pk} успешно запущена!')
#
#     # Возвращаемся на страницу деталей рассылки
#     return redirect('mailing:mailing_detail', pk=pk)
#
#
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Регистрация прошла успешно!')
#             return redirect('mailing:home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm, CustomUserCreationForm
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

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'
    ordering = ['full_name']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()  # Менеджер видит всё
        return Client.objects.filter(owner=user)  # Обычный пользователь видит только своё


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент "%(full_name)s" успешно добавлен!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент "%(full_name)s" успешно обновлён!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    success_message = 'Клиент успешно удалён!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для сообщений ====================

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение "%(subject)s" успешно создано!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение "%(subject)s" успешно обновлено!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')
    success_message = 'Сообщение успешно удалено!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для рассылок ====================

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    ordering = ['-start_time']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно создана!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно обновлена!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Рассылка успешно удалена!'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# ==================== Ручной запуск рассылки ====================

def send_mailing_view(request, pk):
    """Представление для ручного запуска рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверяем, что пользователь является владельцем рассылки или менеджером
    user = request.user
    if not (user.groups.filter(name='Менеджеры').exists() or mailing.owner == user):
        messages.error(request, 'У вас нет прав для запуска этой рассылки.')
        return redirect('mailing:mailing_list')

    # Запускаем отправку
    send_mailing(pk)

    # Показываем сообщение об успехе
    messages.success(request, f'Рассылка #{pk} успешно запущена!')

    # Возвращаемся на страницу деталей рассылки
    return redirect('mailing:mailing_detail', pk=pk)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('mailing:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

