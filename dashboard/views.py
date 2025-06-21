from django.shortcuts import render
import pandas as pd

from analytics import models
from django.db.models import Count, Sum
from crm.models import Order, Client
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns


def dashboard_view(request):
    # Основные метрики
    total_clients = Client.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'total_clients': total_clients,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'dashboard/dashboard.html', context)


def sales_report(request):
    # Анализ продаж
    orders = Order.objects.all().values('created_at', 'total_amount')
    df = pd.DataFrame(orders)

    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['month'] = df['created_at'].dt.to_period('M')
        monthly_sales = df.groupby('month')['total_amount'].sum().reset_index()

        # Создание графика
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=monthly_sales, x='month', y='total_amount')
        plt.title('Monthly Sales Report')
        plt.xlabel('Month')
        plt.ylabel('Total Amount')
        plt.tight_layout()

        # Сохранение графика в base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        context = {'chart': image_base64}
    else:
        context = {'error': 'No data available'}

    return render(request, 'dashboard/sales_report.html', context)


def client_analytics(request):
    # Анализ клиентов
    clients = Client.objects.annotate(
        order_count=Count('order'),
        total_spent=Sum('order__total_amount')
    ).filter(order_count__gt=0)

    # Топ клиентов
    top_clients = clients.order_by('-total_spent')[:10]

    context = {'top_clients': top_clients}
    return render(request, 'dashboard/client_analytics.html', context)
