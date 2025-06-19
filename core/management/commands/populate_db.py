from django.core.management.base import BaseCommand
from core.models import User, Profile  # Импортируем кастомную модель пользователя
from crm.models import Client, Product, Order, OrderItem, SupportTicket
import random
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Populates database with sample data'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Удаляем старые данные (кроме суперпользователей)
            User.objects.filter(is_superuser=False).delete()
            Client.objects.all().delete()
            Product.objects.all().delete()
            Order.objects.all().delete()
            OrderItem.objects.all().delete()
            SupportTicket.objects.all().delete()

            # Получаем или создаем группы
            managers_group, _ = Group.objects.get_or_create(name='Managers')
            analysts_group, _ = Group.objects.get_or_create(name='Analysts')

            # Создаем пользователей-менеджеров
            managers = []
            for i in range(1, 4):
                user = User.objects.create_user(
                    username=f'manager{i}',
                    email=f'manager{i}@example.com',
                    password='password',
                    first_name=f'Manager{i}',
                    last_name='Test'
                )
                user.groups.add(managers_group)
                Profile.objects.create(user=user, phone=f'+7{random.randint(9000000000, 9999999999)}')
                managers.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created manager: {user.username}'))

            # Создаем аналитиков
            analysts = []
            for i in range(1, 3):
                user = User.objects.create_user(
                    username=f'analyst{i}',
                    email=f'analyst{i}@example.com',
                    password='password',
                    first_name=f'Analyst{i}',
                    last_name='Test'
                )
                user.groups.add(analysts_group)
                Profile.objects.create(user=user, phone=f'+7{random.randint(9000000000, 9999999999)}')
                analysts.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created analyst: {user.username}'))

            # Создаем клиентов
            clients = []
            for i in range(1, 51):
                client = Client.objects.create(
                    name=f'Client {i}',
                    email=f'client{i}@example.com',
                    phone=f'+7{random.randint(9000000000, 9999999999)}',
                    manager=random.choice(managers)
                )
                clients.append(client)

                # Создаем товары
                products = []
                for i in range(1, 21):
                    product = Product.objects.create(
                        name=f'Product {i}',
                        price=round(random.uniform(100, 5000), 2),
                        category=random.choice(['digital', 'physical']),
                        stock=random.randint(0, 100),
                        description=f"Description for product {i}"
                    )
                products.append(product)

                # Создаем заказы
                for i in range(1, 101):
                    client = random.choice(clients)
                order_date = datetime.now() - timedelta(days=random.randint(0, 180))

                order = Order.objects.create(
                    client=client,
                    status=random.choice(['pending', 'paid', 'shipped', 'delivered', 'cancelled']),
                    total_amount=0,
                    created_at=order_date
                )

                # Добавляем товары в заказ
                order_items = []
                order_total = 0
                for _ in range(random.randint(1, 5)):
                    product = random.choice(products)
                quantity = random.randint(1, 3)
                item_price = round(product.price * quantity, 2)

                order_items.append(OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                ))
                order_total += item_price

                # Сохраняем элементы заказа
                OrderItem.objects.bulk_create(order_items)
                order.total_amount = round(order_total, 2)
                order.save()

                # Создаем тикеты поддержки
                for i in range(1, 31):
                    SupportTicket.objects.create(
                        client=random.choice(clients),
                        subject=f"Support ticket #{i}",
                        description=f"Description for support ticket #{i}",
                        status=random.choice(['open', 'in_progress', 'resolved', 'closed']),
                        assigned_to=random.choice(managers + analysts)
                    )

                self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))
