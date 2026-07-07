from django.core.management.base import BaseCommand
from mailing.services import send_mailing


class Command(BaseCommand):
    help = 'Отправляет рассылку по её ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            send_mailing(mailing_id)
            self.stdout.write(
                self.style.SUCCESS(f'Рассылка #{mailing_id} успешно отправлена')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {e}')
            )
