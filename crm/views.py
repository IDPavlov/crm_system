from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import csv
from io import TextIOWrapper

from core.models import User
from .models import Client, Product, Order, SupportTicket
from .forms import ClientForm, ProductForm, OrderForm, SupportTicketForm, CSVUploadForm
from django.views.generic import TemplateView


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


class ProductListView(ListView):
    model = Product
    template_name = 'crm/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


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


class SupportTicketCreateView(CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'crm/ticket_form.html'
    success_url = reverse_lazy('ticket_list')


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
