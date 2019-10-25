from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url

from django.http import HttpResponse

def authorize(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            return HttpResponse(status=401)
            
        return _wrapped_view
    return decorator