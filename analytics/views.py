from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from analytics import models
from crm.models import Order, Client
import seaborn as sns


def sales_prediction(request):
    if not request.user.has_perm('analytics.view_salesprediction'):
        return render(request, '403.html', status=403)

    # Загрузка данных
    orders = Order.objects.all().values('created_at', 'total_amount')
    df = pd.DataFrame(orders)

    if len(df) < 10:
        return render(request, 'analytics/sales_prediction.html', {'error': 'Not enough data'})

    # Подготовка данных
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['day_num'] = (df['created_at'] - df['created_at'].min()).dt.days

    X = df[['day_num']].values
    y = df['total_amount'].values

    # Полиномиальная регрессия
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    # Прогноз на 30 дней вперед
    future_days = np.arange(X.max(), X.max() + 30).reshape(-1, 1)
    future_poly = poly.transform(future_days)
    future_pred = model.predict(future_poly)

    # Визуализация
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=X.ravel(), y=y, label='Actual Sales')
    plt.plot(np.concatenate([X.ravel(), future_days.ravel()]),
             np.concatenate([model.predict(X_poly), future_pred]),
             color='red', label='Prediction')
    plt.title('Sales Prediction')
    plt.xlabel('Days')
    plt.ylabel('Sales Amount')
    plt.legend()

    # Сохранение в base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    context = {'chart': image_base64}
    return render(request, 'analytics/sales_prediction.html', context)


def client_segmentation(request):
    if not request.user.has_perm('analytics.view_clientsegmentation'):
        return render(request, '403.html', status=403)

    # Получаем данные клиентов
    clients = Client.objects.annotate(
        order_count=models.Count('order'),
        total_spent=models.Sum('order__total_amount')
    ).filter(order_count__gt=0).values('order_count', 'total_spent')

    if len(clients) < 5:
        return render(request, 'analytics/client_segmentation.html',
                      {'error': 'Недостаточно данных для анализа'})

    # Преобразуем в DataFrame
    df = pd.DataFrame(list(clients))

    # Масштабируем данные
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    # Кластеризация K-Means
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    df['cluster'] = clusters

    # Визуализация
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='total_spent', y='order_count',
                    hue='cluster', palette='viridis', s=100)
    plt.title('Сегментация клиентов')
    plt.xlabel('Общая сумма покупок')
    plt.ylabel('Количество заказов')

    # Сохраняем график
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Описание кластеров
    cluster_descriptions = []
    for cluster in sorted(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster]
        description = {
            'id': cluster,
            'count': len(cluster_data),
            'avg_spent': cluster_data['total_spent'].mean(),
            'avg_orders': cluster_data['order_count'].mean()
        }
        cluster_descriptions.append(description)

    return render(request, 'analytics/client_segmentation.html', {
        'chart': image_base64,
        'clusters': cluster_descriptions
    })
