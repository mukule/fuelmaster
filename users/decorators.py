from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from functools import wraps


def user_not_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator


def superuser(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.access_level == 1:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(render(request, 'users/not_allowed.html'))

    return _wrapped_view


def admin(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.access_level in [1, 2]:  # Admin or Manager
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(render(request, 'users/not_allowed.html'))

    return _wrapped_view


def manager(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Admin, Manager, or Cashier
        if request.user.access_level in [1, 2, 3]:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(render(request, 'users/not_allowed.html'))

    return _wrapped_view


def cashier(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Admin, Manager, or Cashier
        if request.user.access_level in [1, 2, 3, 4]:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(render(request, 'users/not_allowed.html'))

    return _wrapped_view


def company(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.company:
            # Redirect to the main index page if user doesn't belong to any company
            return redirect('main:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
