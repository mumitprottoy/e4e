import json
from django.contrib.auth import models, authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from utils.global_context import Context
from .processor import PaymentProcessor
from sales.models import Channel
from edtech import settings
from utils import decorators
from . import models


@decorators.login_required
def upgrade_to_premium(request):
    context = Context.get_context()
    if request.POST:
        coupon_code = request.POST.get('coupon_code')
        channel = Channel.objects.filter(coupon_code = coupon_code)
        if channel.exists():
            channel = channel.first()
            return redirect('/purchase/'+channel.key)
        else:context['errors'] = ['Invalid coupon code']
    context['form_data'] = {
        'form_header': 'Do you have a coupon code?',
        'input_type': 'text',
        'input_name': 'coupon_code',
        'input_placeholder': 'Coupon code',
        'submit_btn_text': 'Next'
    }
    return render(request, 'payment/coupon_code.html', context)


def purchase_through_link(request, key: str):
    context = Context.get_context()
    channel = Channel.objects.filter(key=key)
    if channel.exists():
        channel = channel.first()
        if not request.user.is_authenticated:
            request.session['login_redirect_url'] = '/purchase/'+channel.key
            return redirect('login')
        processor = PaymentProcessor(user=request.user, key=channel.key)
        purchase = processor.initiate_purchaseV3()
        if not purchase.is_closed:
            if request.POST: 
                gateway = processor.request_gateway(purchase)
                if purchase.is_payable:
                    if gateway is not None:
                        return redirect(gateway)
                
            if purchase.window_is_closed:
                context['purchase'] = purchase
                return render(request, 'payment/try_again_after.html', context)
            context['purchase'] = purchase
            return render(request, 'payment/proceed_to_payment.html', context)
        return render(request, 'payment/paid.html', context)
    context['failure_msg'] = 'Invalid link for purchase'
    return render(request, 'failure_page.html', context)
        

@csrf_exempt
@decorators.login_required                
def payment_response(request, transaction_id: str):
    purchase = models.PurchaseV3.objects.filter(transaction_id=transaction_id)
    if purchase.exists():
        purchase = purchase.first()
        if request.POST:
           pass 

    