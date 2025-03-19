from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import User, QRCode, QRScan
from .forms import UserRegistrationForm


def register_user(request):
    """Страница регистрации пользователя"""
    if request.session.get("user_id"):
        # Если уже зарегистрирован – перенаправляем на страницу с баллами
        return redirect("user_dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.total_points = 1  # Первый балл за регистрацию
            user.save()
            request.session["user_id"] = str(user.user_id)  # Сохраняем в сессии
            return redirect("user_dashboard")  # Перенаправляем на личный кабинет
    else:
        form = UserRegistrationForm()

    return render(request, "contest/register.html", {"form": form})


def process_qr(request):
    """Обработка сканирования QR-кода"""
    qr_code_value = request.GET.get("qr")  # Извлекаем код QR из URL
    if not qr_code_value:
        return JsonResponse({"error": "QR-код не найден"}, status=400)

    # Проверяем, есть ли этот QR-код в базе
    qr_code = get_object_or_404(QRCode, code=qr_code_value)

    user_id = request.session.get("user_id")
    if not user_id:
        # Если пользователь не зарегистрирован, отправляем его на регистрацию
        return redirect("register_user")

    user = get_object_or_404(User, user_id=user_id)

    # Проверяем, сканировал ли он уже этот QR-код
    if QRScan.objects.filter(user=user, qr_code=qr_code).exists():
        message = "Этот QR-код уже был использован!"
    else:
        QRScan.objects.create(user=user, qr_code=qr_code)
        user.total_points += 1
        user.save()
        message = "Баллы начислены!"

    return render(request, "contest/user_dashboard.html", {"user": user, "message": message})


def user_dashboard(request):
    """Страница личного кабинета пользователя"""
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("register_user")

    user = get_object_or_404(User, user_id=user_id)
    return render(request, "contest/user_dashboard.html", {"user": user})


def rankingView(request):
    return render(request, "contest/ranking.html")


def walkthroughView(request):
    return render(request, "contest/walkthrough.html")



from django.http import JsonResponse
from django.views import View
from django.db.models import Sum
from .models import User, Department

class RealTimeRankingView(View):
    """API для подсчета рейтинга в реальном времени"""

    def get(self, request):
        # Топ-5 департаментов (сумма баллов пользователей)
        departments = (
            Department.objects.annotate(total_score=Sum('user__total_points'))
            .order_by('-total_score')[:10]
        )

        department_ranking = [
            {"department": dept.name, "total_score": dept.total_score or 0}
            for dept in departments
        ]

        # Топ-10 пользователей по баллам
        users = User.objects.order_by('-total_points')[:10]

        user_ranking = [
            {"username": user.name, "score": user.total_points, "department": user.department.name if user.department else None}
            for user in users
        ]

        return JsonResponse({
            "department_ranking": department_ranking,
            "user_ranking": user_ranking
        })
