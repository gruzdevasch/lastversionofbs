from django import forms
from django.db.models import Q
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (
    CharFilter, ChoiceFilter, DateFromToRangeFilter, NumberFilter,
    OrderingFilter, RangeFilter)
from payments import PaymentStatus

from ...core.filters import SortedFilterSet
from ...order import SuplierOrderStatus
from ...order.models import Order, SuplierOrder
from ..widgets import DateRangeWidget, MoneyRangeWidget

SORT_BY_FIELDS = [
    ('pk', 'pk'),
    ('status', 'payment_status'),
    ('total_net', 'total')]

SORT_BY_FIELDS_LABELS = {
    'pk': pgettext_lazy('Order list sorting option', '#'),
    'payments__status': pgettext_lazy('Order list sorting option', 'Статус'),
    'total_net': pgettext_lazy('Order list sorting option', 'Оплата')}


class SuplierOrderFilter(SortedFilterSet):
    id = NumberFilter(
        label=pgettext_lazy('Order list filter label', 'ID'))
    status = ChoiceFilter(
        label=pgettext_lazy(
            'Order list filter label', 'Статус'),
        choices=SuplierOrderStatus.CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)
    total_net = RangeFilter(
        label=pgettext_lazy('Order list filter label', 'Итого'),
        widget=MoneyRangeWidget)
    sort_by = OrderingFilter(
        label=pgettext_lazy('Order list filter label', 'Сортировать по'),
        fields=SORT_BY_FIELDS,
        field_labels=SORT_BY_FIELDS_LABELS)

    class Meta:
        model = SuplierOrder
        fields = []


    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard orders list',
            'Found %(counter)d matching order',
            'Found %(counter)d matching orders',
            number=counter) % {'counter': counter}
