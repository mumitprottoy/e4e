import threading
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as logout_user
from django.contrib.auth.models import User
from . import operations as ops
from utils import global_context, keygen, decorators, operations as util_ops


@decorators.loggedin_disallowed
def auth_email(request):
    context = global_context.Context.get_context()
    if request.POST:
        email = request.POST.get('email')
        request.session['user_auth_email'] = email
        auth_key = keygen.KeyGen().alphanumeric_key()
        request.session['auth_key'] = auth_key
        user = User.objects.filter(email=email)
        if not user.exists(): user = ops.create_quick_user(email)
        else: user = user.first()
        if user.codes.is_verified: return redirect('/auth-pwd/'+auth_key)
        # create new user and send verification code through email 
        threading.Thread(target=user.codes.send_verification_code).start()
        return redirect('/auth-codes/verification-code/'+auth_key)
    context.update(util_ops.create_form_data(
        'Enter your email', 'email', 'email', 'leo.messi@miami.club', 'Next'))
    context['google_login_option'] = True
    return render(request, 'entrance/single_input.html', context)


@decorators.loggedin_disallowed
def auth_pwd(request, key: str):
    try:
        assert request.session['auth_key'] == key
        user = User.objects.get(email=request.session['user_auth_email'])
        context = global_context.Context.get_context()
        if request.POST:
            password = request.POST.get('password')
            user_logged_in = ops.login_user(request, username=user.username, password=password)
            if user_logged_in: 
                request.session['auth_key'] = None
                request.session['user_auth_email'] = None
                return redirect('/')
            context['errors'] = ['Wrong password']
        context.update(util_ops.create_form_data(
            'Enter password', 'password', 'password', 'Password', 'Login'))
        context['google_login_option'] = True
        context['auth_pwd'] = True
        return render(request, 'entrance/single_input.html', context)
    except Exception as e: 
        print(e)
        return redirect('nope')


@decorators.loggedin_disallowed
def forgot_password(request):
    try:
        auth_key = request.session['auth_key']
        assert auth_key is not None
        # send otp
        user = User.objects.get(email=request.session['user_auth_email'])
        threading.Thread(target=user.codes.send_otp).start()
        return redirect('/auth-codes/otp/'+auth_key)
    except Exception as e: 
        print(e)
        return redirect('nope')


@decorators.loggedin_disallowed
def auth_codes(request, code_type: str, key:str):
    try:
        code_type = {'otp': 'otp', 'verification-code': 'verification_code'}[code_type]
        assert request.session['auth_key'] == key
        user = User.objects.get(email=request.session['user_auth_email'])
        context = global_context.Context.get_context()
        if request.POST:
            code = request.POST.get(code_type)
            if user.codes.__dict__[code_type] == code: 
                request.session['auth_key'] = None
                request.session['user_auth_email'] = None
                login(request, user)
                if code_type == 'verification_code':
                    user.codes.verify_email()
                    user.codes.change_verification_code()
                else: user.codes.change_otp()
                return redirect('/')
            context['errors'] = ['Invalid code']
        context.update(util_ops.create_form_data(
            'Please check your email', 'tel', code_type, ' '.join(code_type.capitalize().split('_')), 'Submit'))
        return render(request, 'entrance/single_input.html', context)
    except Exception as e: 
        print('Errors:', e)
        return redirect('nope')


def logout(request):
    logout_user(request)
    return redirect('login')