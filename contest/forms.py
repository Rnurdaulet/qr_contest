from django import forms
from .models import User, Department

class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Выберите отдел",
        widget=forms.Select(attrs={"class": "form-select rounded-xs"})
    )

    class Meta:
        model = User
        fields = ["name", "department"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-xs", "placeholder": "Введите ваше имя"}),
        }
