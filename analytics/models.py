from django.db import models

class AnalyticsPermissions(models.Model):
    """
    Фиктивная модель для создания кастомных разрешений
    """
    class Meta:
        managed = False  # Не создаёт таблицу в БД
        permissions = [
            ('view_salesprediction', 'Can view sales prediction'),
            ('view_clientsegmentation', 'Can view client segmentation'),
        ]