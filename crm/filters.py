import django_filters
from .models import SupportTicket


class SupportTicketFilter(django_filters.FilterSet):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решен'),
        ('closed', 'Закрыт'),
    ]

    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        label='Статус',
        empty_label='Все статусы'
    )

    class Meta:
        model = SupportTicket
        fields = ['status', 'assigned_to']