from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from crm.models import Client, Order
import random


def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            client = Client.objects.get(email=email)
            otp = str(random.randint(100000, 999999))

            # Сохраняем все нужные данные клиента в сессии
            request.session['client_auth'] = {
                'otp': otp,
                'email': email,
                'client_id': client.id,  # Добавляем ID клиента
                'name': client.name  # Можно добавить другие часто используемые поля
            }

            send_mail(
                'Your Login Code',
                f'Your OTP is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('client_verify_otp')
        except Client.DoesNotExist:
            messages.error(request, 'Client not found')
    return render(request, 'core/client_login.html')


def client_verify_otp(request):
    if not request.session.get('client_auth'):
        return redirect('client_login')

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if user_otp == request.session['client_auth']['otp']:
            # Переносим client_id в отдельную переменную сессии для удобства
            request.session['client_id'] = request.session['client_auth']['client_id']
            return redirect('client_dashboard')
        messages.error(request, 'Invalid OTP')
    return render(request, 'core/client_verify_otp.html')


def client_dashboard(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('client_login')

    # Получаем клиента из БД (можно добавить кеширование)
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client)

    return render(request, 'core/client_dashboard.html', {
        'client': client,
        'orders': orders
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Проверка секретного ключа для аналитиков
            if form.cleaned_data['secret_key'] == settings.ANALYST_SECRET_KEY:
                group = Group.objects.get(name='Analysts')
                user.groups.add(group)

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'core/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'core/logout.html'


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/profile.html', {'form': form})
