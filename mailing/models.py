from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator


# Create your models here.

class Client(models.Model):
    """
    Модель получателя рассылки (клиента)
    """
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Введите email получателя'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='Ф. И. О.',
        help_text='Введите фамилию, имя и отчество'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий',
        help_text='Дополнительная информация о клиенте'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='clients',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['full_name']


class Message(models.Model):
    """
    Модель сообщения для рассылки
    """
    subject = models.CharField(
        max_length=255,
        verbose_name='Тема письма',
        help_text='Введите тему сообщения'
    )
    body = models.TextField(
        verbose_name='Тело письма',
        help_text='Введите текст сообщения'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='messages',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.subject[:50]

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']


class Mailing(models.Model):
    """
    Модель рассылки. Статус вычисляется динамически на основе текущего времени.
    """
    # Статусы рассылки
    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    start_time = models.DateTimeField(
        verbose_name='Дата и время начала отправки',
        help_text='Укажите дату и время, когда рассылка должна начаться'
    )
    end_time = models.DateTimeField(
        verbose_name='Дата и время окончания отправки',
        help_text='Укажите дату и время, когда рассылка должна закончиться'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name='Статус'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Сообщение',
        help_text='Выберите сообщение для рассылки'
    )
    recipients = models.ManyToManyField(
        Client,
        related_name='mailings',
        verbose_name='Получатели',
        help_text='Выберите получателей рассылки'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='mailings',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Рассылка #{self.id} - {self.message.subject[:30]}"

    def update_status(self):
        """
        Вычисляет текущий статус и обновляет его в базе данных, если он изменился.
        """
        now = timezone.now()
        new_status = None

        if now < self.start_time:
            new_status = 'Создана'
        elif self.start_time <= now <= self.end_time:
            new_status = 'Запущена'
        else:
            new_status = 'Завершена'

        # Если статус изменился — обновляем его в БД
        if self.status != new_status:
            self.status = new_status
            # Сохраняем только поле status, чтобы не задеть другие поля
            Mailing.objects.filter(pk=self.pk).update(status=new_status)

        return self.status

    def save(self, *args, **kwargs):
        """
        При создании новой рассылки автоматически вычисляем статус.
        """
        if not self.pk:  # Если это новая запись
            now = timezone.now()
            if now < self.start_time:
                self.status = 'Создана'
            elif self.start_time <= now <= self.end_time:
                self.status = 'Запущена'
            else:
                self.status = 'Завершена'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-start_time']
        permissions = [
            ("can_view_all_mailings", "Can view all mailings"),
            ("can_disable_mailings", "Can disable mailings"),
        ]


class MailingAttempt(models.Model):
    """
    Модель попытки рассылки (логи отправки)
    """

    # Статусы попытки
    STATUS_SUCCESS = 'Успешно'
    STATUS_FAILED = 'Не успешно'

    ATTEMPT_STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно'),
    ]

    attempt_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки',
        help_text='Автоматически фиксируется при создании записи'
    )
    status = models.CharField(
        max_length=20,
        choices=ATTEMPT_STATUS_CHOICES,
        verbose_name='Статус попытки'
    )
    server_response = models.TextField(
        blank=True,
        verbose_name='Ответ почтового сервера',
        help_text='Текст ошибки или подтверждение отправки'
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка'
    )

    def __str__(self):
        return f"Попытка #{self.id} - {self.mailing} - {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        ordering = ['-attempt_datetime']
