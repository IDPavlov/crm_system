from django import forms
from .models import Client, Product, Order, SupportTicket, User


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
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Order
        fields = ['client', 'status', 'products', 'total_amount']


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['client', 'subject', 'description', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Опционально: ограничить выбор пользователей только менеджерами
        self.fields['assigned_to'].queryset = User.objects.filter(
            groups__name='Managers'
        )


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()