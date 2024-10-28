from django.shortcuts import redirect
from django.contrib import messages


def superuser_required(view_func, login_url="login"):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(login_url)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
