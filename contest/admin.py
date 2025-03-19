# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, QRCode, QRScan, Department

@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    """Справочник отделов"""
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(ModelAdmin):
    """Пользователи"""
    list_display = ("name", "department", "total_points")
    search_fields = ("name", "department__name")
    list_filter = ("department",)

    fieldsets = (
        ("Основная информация", {"fields": ("name", "department")}),
        ("Баллы", {"fields": ("total_points",)}),
    )

@admin.register(QRCode)
class QRCodeAdmin(ModelAdmin):
    """QR-коды"""
    list_display = ("code", "created_at", "qr_image_preview")
    search_fields = ("code",)
    readonly_fields = ("qr_image",)

    def qr_image_preview(self, obj):
        if obj.qr_image:
            return f'<img src="{obj.qr_image.url}" width="50">'
        return "Нет изображения"

    qr_image_preview.allow_tags = True
    qr_image_preview.short_description = "QR-код"

@admin.register(QRScan)
class QRScanAdmin(ModelAdmin):
    """Сканирования QR-кодов"""
    list_display = ("user", "qr_code", "timestamp")
    search_fields = ("user__name", "qr_code__code")
    list_filter = ("timestamp",)
