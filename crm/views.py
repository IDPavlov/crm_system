from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import csv
from io import TextIOWrapper

from core.models import User
from .models import Client, Product, Order, SupportTicket
from .forms import ClientForm, ProductForm, OrderForm, SupportTicketForm, CSVUploadForm


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


# Аналогичные представления для Product, Order, SupportTicket...

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