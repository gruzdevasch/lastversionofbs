from django.conf.urls import url

from . import views
from ..core import TOKEN_PATTERN

urlpatterns = [
    url(r'^%s/$' % (TOKEN_PATTERN,), views.details, name='details'),
    url(r'^%s/payment/$' % (TOKEN_PATTERN,),
        views.payment, name='payment'),
    url(r'^%s/payment/(?P<variant>[-\w]+)/$' % (TOKEN_PATTERN,),
        views.start_payment, name='payment'),
    url(r'^%s/cancel-payment/$' % (TOKEN_PATTERN,), views.cancel_payment,
        name='cancel-payment'),
    url(r'^%s/payment-success/$' % (TOKEN_PATTERN,),
        views.payment_success, name='payment-success'),
    url(r'checkout-success/',
        views.checkout_success, name='checkout-success'),
    url(r'handlew1/',
        views.checkout_handling, name='checkout-handling'),
    url(r'checkout-fail/',
        views.checkout_fail, name='checkout-fail'),
    url(r'^%s/attach/$' % (TOKEN_PATTERN,),
        views.connect_order_with_user, name='connect-order-with-user'),
]
