from django import forms
from django.utils import timezone
from .models import Client, Message, Mailing
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Дополнительная информация'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема письма'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Текст сообщения...'}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'message': forms.Select(attrs={'class': 'form-select'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
            raise forms.ValidationError('Дата и время начала не могут быть в прошлом.')
        return start_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('Дата и время окончания должны быть позже даты начала.')
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
