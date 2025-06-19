from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.CRMDashboardView.as_view(), name='crm_dashboard'),
    # Clients
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Orders
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # Support Tickets
    path('tickets/', views.SupportTicketListView.as_view(), name='ticket_list'),
    path('tickets/create/', views.SupportTicketCreateView.as_view(), name='ticket_create'),
    path('tickets/<int:pk>/', views.SupportTicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/update/', views.SupportTicketUpdateView.as_view(), name='ticket_update'),
    path('tickets/<int:pk>/delete/', views.SupportTicketDeleteView.as_view(), name='ticket_delete'),

    # CSV Import
    path('import/clients/', views.import_clients, name='import_clients'),
]