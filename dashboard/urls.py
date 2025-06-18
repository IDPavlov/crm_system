from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('client-analytics/', views.client_analytics, name='client_analytics'),
]