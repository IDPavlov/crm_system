from django.urls import path
from . import views

urlpatterns = [
    path('sales-prediction/', views.sales_prediction, name='sales_prediction'),
    path('client-segmentation/', views.client_segmentation, name='client_segmentation'),
]