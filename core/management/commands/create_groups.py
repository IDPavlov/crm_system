from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates default user groups and permissions'

    def handle(self, *args, **options):
        # Создаём группы
        managers, _ = Group.objects.get_or_create(name='Managers')
        analysts, _ = Group.objects.get_or_create(name='Analysts')

        # Базовые права для менеджеров
        manager_perms = Permission.objects.filter(
            codename__in=[
                'add_client', 'change_client', 'view_client',
                'add_order', 'change_order', 'view_order',
                'view_product'
            ]
        )
        managers.permissions.set(manager_perms)

        # Базовые права для аналитиков
        analyst_perms = Permission.objects.filter(
            codename__in=[
                'view_client', 'view_order', 'view_product'
            ]
        )
        analysts.permissions.set(analyst_perms)

        # Добавляем кастомные права аналитики
        custom_perms = Permission.objects.filter(
            codename__in=[
                'view_salesprediction',
                'view_clientsegmentation'
            ]
        )
        if custom_perms.exists():
            analysts.permissions.add(*custom_perms)
            self.stdout.write(self.style.SUCCESS('Added custom permissions to Analysts group'))
        else:
            self.stdout.write(self.style.WARNING('Custom permissions not found'))

        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))