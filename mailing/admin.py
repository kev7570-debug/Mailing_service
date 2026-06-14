from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body_preview')
    search_fields = ('subject',)

    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body

    body_preview.short_description = 'Тело письма (превью)'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime', 'status', 'message')
    list_filter = ('status', 'start_datetime')
    filter_horizontal = ('recipients',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_datetime', 'status', 'mailing', 'server_response')
    list_filter = ('status', 'attempt_datetime')
