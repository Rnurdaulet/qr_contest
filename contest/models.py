import uuid
import segno
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models

class Department(models.Model):
    """Справочник отделов"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    """Модель пользователя"""
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  # Ссылка на отдел
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.department})"

class QRCode(models.Model):
    """Модель QR-кода"""
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Уникальный UUID
    description = models.TextField(blank=True, null=True)  # Описание QR
    qr_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)  # QR-картинка
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def qr_full_url(self):
        """Генерирует полный URL QR-кода"""
        return f"{settings.QR_URL}?qr={self.code}"

    def generate_qr(self):
        """Генерирует изображение QR-кода с `segno` на основе `QR_URL + UUID`"""
        qr = segno.make(self.qr_full_url)  # Создаем QR для ссылки
        buffer = BytesIO()
        qr.save(buffer, kind="png", scale=5)
        return ContentFile(buffer.getvalue(), name=f"qr_{self.code}.png")

    def save(self, *args, **kwargs):
        """Создание QR-кода перед сохранением"""
        if not self.qr_image:
            self.qr_image.save(f"qr_{self.code}.png", self.generate_qr(), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR {self.code} - {self.qr_full_url}"

class QRScan(models.Model):
    """Модель сканирования QR-кодов пользователями"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "qr_code")  # Один пользователь может сканировать QR только один раз
