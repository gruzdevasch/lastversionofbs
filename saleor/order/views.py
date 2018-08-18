import logging

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponse
from django.utils.translation import pgettext_lazy
from django.views.decorators.csrf import csrf_exempt
from payments import PaymentStatus, RedirectNeeded
from ..checkout.models import Cart
from ..checkout.utils import create_order, get_taxes_for_cart
from ..order import OrderStatus, SuplierOrderStatus, CustomPaymentChoices
from ..core import analytics
from ..core.exceptions import InsufficientStock
from .emails import send_order_confirmation
from . import FulfillmentStatus
from ..account.forms import LoginForm
from ..account.models import User, Address
from ..core.utils import get_client_ip
from .forms import (
    OrderNoteForm, PasswordForm, PaymentDeleteForm, PaymentMethodsForm)
from .models import Order, OrderNote, Payment, SuplierOrder
from .utils import attach_order_to_user, check_order_status
import hashlib
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import EmailMessage, EmailMultiAlternatives
logger = logging.getLogger(__name__)


def details(request, token):
    orders = Order.objects.confirmed().prefetch_related(
        'lines__variant', 'fulfillments', 'fulfillments__lines',
        'fulfillments__lines__order_line')
    orders = orders.select_related('user')
    order = get_object_or_404(orders, token=token)
    notes = order.notes.filter(is_public=True)
    ctx = {'order': order, 'notes': notes}
    if order.is_open():
        user = request.user if request.user.is_authenticated else None
        note = OrderNote(order=order, user=user)
        note_form = OrderNoteForm(request.POST or None, instance=note)
        ctx.update({'note_form': note_form})
        if request.method == 'POST':
            if note_form.is_valid():
                note_form.save()
                return redirect('order:details', token=order.token)
    fulfillments = order.fulfillments.filter(
        status=FulfillmentStatus.FULFILLED)
    ctx.update({'fulfillments': fulfillments})
    return TemplateResponse(request, 'order/details.html', ctx)


def payment(request, token):
    orders = Order.objects.confirmed().filter(billing_address__isnull=False)
    orders = orders.prefetch_related('lines__variant')
    orders = orders.select_related(
        'billing_address', 'shipping_address', 'user')
    order = get_object_or_404(orders, token=token)
    payments = order.payments.all()
    form_data = request.POST or None
    try:
        waiting_payment = order.payments.get(status=PaymentStatus.WAITING)
    except Payment.DoesNotExist:
        waiting_payment = None
        waiting_payment_form = None
    else:
        form_data = None
        waiting_payment_form = PaymentDeleteForm(
            None, order=order, initial={'payment_id': waiting_payment.id})
    if order.is_fully_paid() or not order.billing_address:
        form_data = None
    payment_form = None
    if not order.is_pre_authorized():
        payment_form = PaymentMethodsForm(form_data)
        # FIXME: redirect if there is only one payment method
        if payment_form.is_valid():
            payment_method = payment_form.cleaned_data['method']
            return redirect(
                'order:payment', token=order.token, variant=payment_method)
    ctx = {
        'order': order, 'payment_form': payment_form, 'payments': payments,
        'waiting_payment': waiting_payment,
        'waiting_payment_form': waiting_payment_form}
    return TemplateResponse(request, 'order/payment.html', ctx)


@check_order_status
def start_payment(request, order, variant):
    waiting_payments = order.payments.filter(
        status=PaymentStatus.WAITING).exists()
    if waiting_payments:
        return redirect('order:payment', token=order.token)
    billing = order.billing_address
    total = order.total
    defaults = {
        'total': total.gross.amount,
        'tax': total.tax.amount,
        'currency': total.currency,
        'delivery': order.shipping_price.net.amount,
        'billing_first_name': billing.first_name,
        'billing_last_name': billing.last_name,
        'billing_address_1': billing.street_address_1,
        'billing_address_2': billing.street_address_2,
        'billing_city': billing.city,
        'billing_postcode': billing.postal_code,
        'billing_country_code': billing.country.code,
        'billing_email': order.user_email,
        'description': pgettext_lazy(
            'Payment description', 'Order %(order_number)s') % {
                'order_number': order},
        'billing_country_area': billing.country_area,
        'customer_ip_address': get_client_ip(request)}
    variant_choices = settings.CHECKOUT_PAYMENT_CHOICES
    if variant not in [code for code, dummy_name in variant_choices]:
        raise Http404('%r is not a valid payment variant' % (variant,))
    with transaction.atomic():
        payment, dummy_created = Payment.objects.get_or_create(
            variant=variant, status=PaymentStatus.WAITING, order=order,
            defaults=defaults)
        try:
            form = payment.get_form(data=request.POST or None)
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))
        except Exception:
            logger.exception('Error communicating with the payment gateway')
            msg = pgettext_lazy(
                'Payment gateway error',
                'Oops, it looks like we were unable to contact the selected '
                'payment service')
            messages.error(request, msg)
            payment.change_status(PaymentStatus.ERROR)
            return redirect('order:payment', token=order.token)
    template = 'order/payment/%s.html' % variant
    ctx = {'form': form, 'payment': payment}
    return TemplateResponse(
        request, [template, 'order/payment/default.html'], ctx)


@check_order_status
def cancel_payment(request, order):
    form = PaymentDeleteForm(request.POST or None, order=order)
    if form.is_valid():
        with transaction.atomic():
            form.save()
        return redirect('order:payment', token=order.token)
    return HttpResponseForbidden()


@csrf_exempt
def payment_success(request, token):
    """Receive request from payment gateway after paying for an order.

    Redirects user to payment success.
    All post data and query strings are dropped.
    """
    url = reverse('order:checkout-success', kwargs={'token': token})
    return redirect(url)

@csrf_exempt
def checkout_handling(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user = get_object_or_404(User, email=email)
        notification_type=request.POST.get('notification_type')
        operation_id=request.POST.get('operation_id')        
        amount=request.POST.get('amount')
        withdraw_amount=request.POST.get('withdraw_amount')
        currency=request.POST.get('currency')
        datetime=request.POST.get('datetime')
        sender=request.POST.get('sender')
        city = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        suite = request.POST.get('suite')
        flat = request.POST.get('flat')
        zip = request.POST.get('zip')
        codepro=request.POST.get('codepro')
        notification_secret=settings.YANDEX_SECRET_KEY
        label=request.POST.get('label')
        sha1_hash=request.POST.get('sha1_hash')
        madesha1 = notification_type + '&' + operation_id + '&' + amount + '&' + currency + '&' + datetime + '&' + sender + '&' + codepro + '&' + notification_secret + '&' + label
        sha1_madehash = hashlib.sha1(madesha1.encode('utf-8')).hexdigest()
        if sha1_madehash == sha1_hash:
            cart = Cart.objects.all().filter(user=user).first()
            if city:
                user.delivery_address = city
                user.save()
                """address = Address()
                address.first_name = user.first_name
                address.last_name = user.last_name
                address.company_name = " "
                address.street_address_1 = " "
                address.street_address_2 = " "
                address.city = city
                address.city_area = " "
                address.postal_code = " "
                address.country = "Russian Federation"
                address.country_area = " "
                address.phone = user.phone
                address.save()
                
                
                user.default_billing_address = address
                user.addresses.add(address)
                user.save()
                cart.billing_address = user.addresses.first()
                cart.save()"""
                
            try:
                order = create_order(
                    cart=cart,
                    tracking_code=analytics.get_client_id(request),
                    discounts=request.discounts,
                    taxes=get_taxes_for_cart(cart, request.taxes))
            except InsufficientStock:
                return redirect('cart:index')
          # happens when a voucher is now invalid
            if not order:
                msg = pgettext('Checkout warning', 'Проверьте свою корзину(возможно истек срок действия купона).')
                messages.warning(request, msg)
                return redirect('cart:index')
            cart.delete()
            msg = pgettext_lazy('Order status history entry', 'Заказ размещен.')
            order.history.create(user=user, content=msg)

            lines = order.lines.all()
            for line in lines:
                suplierorder = SuplierOrder.objects.get_or_create(status=SuplierOrderStatus.CURRENT, 
                    suplier = line.variant.product.suplier)[0]
                line.suplierorder = suplierorder
                suplierorder.total_net += line.get_total()
                suplierorder.save()
                line.save()
            order.status = OrderStatus.PAID
            defaults = {
                'total': order.total.gross.amount,
                'tax': order.total.tax.amount,
                'currency': order.total.currency,
                'delivery': order.shipping_price.net.amount,
                'description': pgettext_lazy(
                    'Payment description', 'Order %(order)s') % {
                        'order': order},
                'captured_amount': order.total.gross.amount}
            Payment.objects.get_or_create(
                variant=CustomPaymentChoices.MANUAL,
                status=PaymentStatus.CONFIRMED, order=order,
                defaults=defaults)
            msg = pgettext_lazy(
                'Dashboard message',
                'Заказ был оплачен')
            order.history.create(content=msg, user=user)
            order.save()
            for line in lines:
                suplierorder = line.suplierorder
                if suplierorder.total_net.amount >= 10000:
                    suplierorder.status = SuplierOrderStatus.READY_TO_HANDLE
                    suplieroder.save()
            
            site = Site.objects.get_current()
            mail_subject = 'Заказ на BlitzShop'
            message = render_to_string('templated_email/compiled/confirm_order.html', {
                    'domain': site.domain,
                    'site_name': site.name,
                    'order': order
                })
            to_email = email
            
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()
    return HttpResponse(status_code =200)

def checkout_fail(request):
    return redirect ('/')

def checkout_success(request):
    """Redirect user after placing an order.
    
    Anonymous users are redirected to the checkout success page.
    Registered users are redirected to order details page and the order
    is attached to their account.
    """
    email = request.user.email
    order = Order.objects.all().filter(user_email=email).first()

    ctx = {'email': email, 'order': order}
    return TemplateResponse(request, 'order/checkout_success.html', ctx)


@login_required
def connect_order_with_user(request, token):
    """Connect newly created order to an authenticated user."""
    try:
        order = Order.objects.get(user_email=request.user.email, token=token)
    except Order.DoesNotExist:
        order = None
    if not order:
        msg = pgettext_lazy(
            'Connect order with user warning message',
            "We couldn't assign the order to your account as the email"
            " addresses don't match")
        messages.warning(request, msg)
        return redirect('account:details')
    attach_order_to_user(order, request.user)
    msg = pgettext_lazy(
        'storefront message',
        'The order is now assigned to your account')
    messages.success(request, msg)
    return redirect('order:details', token=order.token)
