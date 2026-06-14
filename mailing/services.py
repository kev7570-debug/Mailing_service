from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt


def send_mailing(mailing_id):
    """
    Отправляет все письма для указанной рассылки
    и создаёт записи о попытках.
    """
    mailing = Mailing.objects.get(id=mailing_id)
    recipients = mailing.recipients.all()

    # Перебираем всех получателей
    for recipient in recipients:
        try:
            # Пытаемся отправить письмо
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL or None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            # Если успешно - создаём запись об успехе
            MailingAttempt.objects.create(
                status='Успешно',
                server_response='Письмо успешно отправлено',
                mailing=mailing,
            )
        except Exception as e:
            # Если ошибка - создаём запись с ошибкой
            MailingAttempt.objects.create(
                status='Не успешно',
                server_response=str(e),
                mailing=mailing,
            )

    # После отправки обновляем статус рассылки
    if mailing.status == 'Создана':
        mailing.status = 'Запущена'
        mailing.save()
