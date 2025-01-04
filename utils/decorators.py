from django.shortcuts import redirect
from django.http import JsonResponse
from django import urls


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['login_redirect_url'] = request.build_absolute_uri()
            return redirect('login')
        return view_func.__call__(request, *args, **kwargs)
    return wrapper


def loggedin_disallowed(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view_func.__call__(request, *args, **kwargs)
    return wrapper


def phone_number_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'phone'):
                return redirect('add-phone-number')
        return view_func.__call__(request, *args, **kwargs)
    return wrapper


def save_next_url(view_func):    
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next_url'] = urls.reverse(
                view_func.__name__, args=args, kwargs=kwargs)
        return view_func.__call__(request, *args, **kwargs)
    return wrapper


def api_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False})
        return view_func.__call__(request, *args, **kwargs)
    return wrapper


def redirect_to_requested_page_after_login(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.is_authenticated: 
                redirect_url = request.session['login_redirect_url']
                if redirect_url is not None:
                    request.session['login_redirect_url'] = None
                    return redirect(redirect_url)
        except: pass 
        return view_func.__call__(request, *args, **kwargs)
    return wrapper