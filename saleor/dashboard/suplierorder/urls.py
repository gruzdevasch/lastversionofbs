from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.order_list, name='suplierorders'),
    url(r'^(?P<order_pk>\d+)/$',
        views.order_details, name='suplierorder-details'),
    url(r'^(?P<order_pk>\d+)/add-note/$',
        views.order_add_note, name='suplierorder-add-note'),
    url(r'^(?P<order_pk>\d+)/edit-discount/$',
        views.order_discount_edit, name='suplierorder-discount-edit'),
    url(r'^(?P<order_pk>\d+)/edit-voucher/$',
        views.order_voucher_edit, name='suplierorder-voucher-edit'),
    url(r'^(?P<order_pk>\d+)/remove-voucher/$',
        views.order_voucher_remove, name='suplierorder-voucher-remove'),
    url(r'^(?P<order_pk>\d+)/delete/$',
        views.remove_draft_order, name='suplierdraft-order-delete'),

    url(r'^(?P<order_pk>\d+)/payment/(?P<payment_pk>\d+)/capture/$',
        views.capture_payment, name='supliercapture-payment'),
    url(r'^(?P<order_pk>\d+)/payment/(?P<payment_pk>\d+)/release/$',
        views.release_payment, name='suplierrelease-payment'),
    url(r'^(?P<order_pk>\d+)/payment/(?P<payment_pk>\d+)/refund/$',
        views.refund_payment, name='suplierrefund-payment'),

    url(r'^(?P<order_pk>\d+)/line/(?P<line_pk>\d+)/change/$',
        views.orderline_change_quantity, name='suplierorderline-change-quantity'),
    url(r'^(?P<order_pk>\d+)/line/(?P<line_pk>\d+)/cancel/$',
        views.orderline_cancel, name='suplierorderline-cancel'),
    url(r'^(?P<order_pk>\d+)/add-variant/$',
        views.add_variant_to_order, name='suplieradd-variant-to-order'),
    url(r'^(?P<order_pk>\d+)/fulfill/$',
        views.fulfill_order_lines, name='suplierfulfill-order-lines'),
    url(r'^(?P<order_pk>\d+)/fulfillment/(?P<fulfillment_pk>\d+)/cancel/$',
        views.cancel_fulfillment, name='suplierfulfillment-cancel'),
    url(r'^(?P<order_pk>\d+)/fulfillment/(?P<fulfillment_pk>\d+)/tracking/$',
        views.change_fulfillment_tracking, name='suplierfulfillment-change-tracking'),
    url(r'^(?P<order_pk>\d+)/fulfillment/(?P<fulfillment_pk>\d+)/packing-slips/$',  # noqa
        views.fulfillment_packing_slips, name='suplierfulfillment-packing-slips'),
    url(r'^(?P<order_pk>\d+)/invoice/$',
        views.order_invoice, name='suplierorder-invoice'),
    url(r'^(?P<order_pk>\d+)/mark-as-paid/$',
        views.mark_order_as_paid, name='suplierorder-mark-as-paid'),]
