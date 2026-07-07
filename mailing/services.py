from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Mailing, MailingAttempt

def send_mailing(mailing_id):
    """
    Отправляет письма для рассылки, проверяя, что текущее время
    находится между start_time и end_time.
    """
    mailing = Mailing.objects.get(id=mailing_id)

    # 1. Проверка времени
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError(
            f"Рассылка может быть отправлена только с {mailing.start_time} по {mailing.end_time}"
        )

    # 2. Определяем получателей
    recipients = mailing.recipients.all()
    attempts_to_create = []

    # 3. Отправляем письма и готовим записи для пакетного создания
    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL or None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            attempts_to_create.append(
                MailingAttempt(
                    status='Успешно',
                    server_response='Письмо успешно отправлено',
                    mailing=mailing,
                )
            )
        except Exception as e:
            attempts_to_create.append(
                MailingAttempt(
                    status='Не успешно',
                    server_response=str(e),
                    mailing=mailing,
                )
            )

    # 4. Пакетное создание записей о попытках (bulk_create)
    if attempts_to_create:
        MailingAttempt.objects.bulk_create(attempts_to_create)

    # 5. Обновляем статус рассылки (он изменится, если время отправки уже прошло)
    mailing.update_status()

    return True
