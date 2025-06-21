from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import csv
from io import TextIOWrapper

from core.models import User
from .filters import SupportTicketFilter
from .models import Client, Product, Order, SupportTicket
from .forms import ClientForm, ProductForm, OrderForm, SupportTicketForm, CSVUploadForm
from django.views.generic import TemplateView

import django_filters
from .models import Order


class CRMDashboardView(TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_clients'] = Client.objects.order_by('-created_at')[:5]
        context['recent_orders'] = Order.objects.order_by('-created_at')[:5]
        return context


class ClientListView(ListView):
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        manager = self.request.GET.get('manager')
        if manager:
            queryset = queryset.filter(manager__id=manager)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = User.objects.filter(groups__name='Managers')
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'crm/client_detail.html'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')


class OrderFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(field_name='client__name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    min_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')

    class Meta:
        model = Order
        fields = []


class ProductListView(ListView):
    model = Product
    template_name = 'crm/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    filterset_class = OrderFilter


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'crm/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'crm/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'crm/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'crm/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


# Order Views
class OrderListView(ListView):
    model = Order
    template_name = 'crm/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'crm/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Убедитесь, что форма есть в контексте
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'crm/order_detail.html'


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'crm/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'crm/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# SupportTicket Views
class SupportTicketListView(ListView):
    model = SupportTicket
    template_name = 'crm/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SupportTicketFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class SupportTicketCreateView(CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'crm/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        # Автоназначение текущего пользователя
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class SupportTicketDetailView(DetailView):
    model = SupportTicket
    template_name = 'crm/ticket_detail.html'


class SupportTicketUpdateView(UpdateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'crm/ticket_form.html'
    success_url = reverse_lazy('ticket_list')


class SupportTicketDeleteView(DeleteView):
    model = SupportTicket
    template_name = 'crm/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket_list')


def import_clients(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            for row in reader:
                Client.objects.create(
                    name=row['name'],
                    email=row['email'],
                    phone=row['phone']
                )
            return redirect('client_list')
    else:
        form = CSVUploadForm()
    return render(request, 'crm/import_clients.html', {'form': form})
