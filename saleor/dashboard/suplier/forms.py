import uuid

from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
from django_prices.forms import MoneyField

from ...product.models import Product, ProductSuplier


class SuplierForm(forms.ModelForm):

    class Meta:
        model = ProductSuplier
        exclude = []
        labels = {
            'name': pgettext_lazy(
                'Sale name','Название')
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        return super().save()


