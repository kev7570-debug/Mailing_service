from django.db import models
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

    # Для отображения в админке и дебаге
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

    def __str__(self):
        # Возвращаем первые 50 символов темы для краткости
        return self.subject[:50]

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']


class Mailing(models.Model):
    """
    Модель рассылки
    """

    # Статусы рассылки (вынесены в отдельный кортеж для удобства)
    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    start_datetime = models.DateTimeField(
        verbose_name='Дата и время первой отправки',
        help_text='Укажите дату и время начала рассылки'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Дата и время окончания отправки',
        help_text='Укажите дату и время окончания рассылки'
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

    def __str__(self):
        return f"Рассылка #{self.id} - {self.message.subject[:30]}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-start_datetime']
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
