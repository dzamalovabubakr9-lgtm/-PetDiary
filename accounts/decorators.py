from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(allowed_roles, login_url='login'):
    """
    Декоратор: разрешает доступ только пользователям с ролью из allowed_roles,
    а также staff и superuser. Анонимов перенаправляет на login_url.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect(login_url)
            if user.is_staff or user.is_superuser:
                return view_func(request, *args, **kwargs)
            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                'Доступ запрещён: у вас нет роли администратора.'
            )
        return wrapped
    return decorator
