from django import forms
from .models import Client, Product, Order, SupportTicket


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['client', 'subject', 'description', 'assigned_to']
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()