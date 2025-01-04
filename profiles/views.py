from django.shortcuts import render
from utils import decorators, global_context, operations as util_ops
from . import models, operations as ops


@decorators.login_required
@decorators.redirect_to_requested_page_after_login
def profile(request):
    context = global_context.Context.get_context()
    return render(request, 'profiles/profile.html', context)

@decorators.login_required
def add_phone_number(request):
    context = global_context.Context.get_context()
    if request.POST:
        phone_number = request.POST.get('phone_number')
        if hasattr(request.user, 'phone'):
            phone = models.Phone.objects.get(user=request.user)      
            phone.number = phone_number; phone.save()
        else: models.Phone(user=request.user, number=phone_number).save()
        return util_ops.redirect_to_success_page(request, 'Phone number is saved.', sl=3, redirect_url='profile')
    context['form_data'] = util_ops.set_form_data(
        'Add phone number', 'tel', 'phone_number', '01876XXXXXX', 'Save')
    return render(request, 'profiles/add_phone_number.html', context)


@decorators.login_required
def update_full_name(request):
    context = global_context.Context.get_context()
    if request.POST:
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if ops.validate_full_name(first_name, last_name):
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return util_ops.redirect_to_success_page(request, 'Your full name is updated.', sl=3, redirect_url='profile')
        context['errors'] = ['Names cannot be empty']
    return render(request, 'profiles/update_full_name.html', context)


@decorators.login_required
def set_password(request):
    context = global_context.Context.get_context()
    if request.POST:
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if len(password) >= 8 and password == confirm_password:
            request.user.set_password(password)
            request.user.save()
            return util_ops.redirect_to_success_page(request, 'Your password is successfully updated.', sl=3, redirect_url='/auth-email')
        context['errors'] = ['Invalid password.']
    return render(request, 'profiles/set_password.html', context)