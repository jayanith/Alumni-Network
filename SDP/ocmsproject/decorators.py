from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required(['admin', 'instructor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'role' not in request.session:
                messages.error(request, 'Please login first!')
                return redirect('login')
            
            if request.session['role'] not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page!')
                return redirect('login')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

