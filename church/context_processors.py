from .models import Department


def department_navigation(request):
    return {
        "nav_departments": Department.objects.filter(is_active=True).only("name", "slug", "order")
    }
