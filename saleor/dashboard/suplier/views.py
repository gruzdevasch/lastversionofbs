from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from . import forms
from ...core.utils import get_paginator_items
from ...product.models import Product, ProductSuplier
from ..views import staff_member_required



@staff_member_required
def suplier_list(request):
    supliers = ProductSuplier.objects.all().order_by('name')
    return TemplateResponse(request, 'dashboard/suplier/list.html', {'supliers': supliers})


@staff_member_required
def suplier_add(request):
    suplier = ProductSuplier()
    form = forms.SuplierForm(request.POST or None, instance=suplier)
    if form.is_valid():
        suplier = form.save()
        msg = pgettext_lazy('Sale (discount) message', 'Добавлен поставщик')
        messages.success(request, msg)
        return redirect('dashboard:suplier-update', pk=suplier.pk)
    ctx = {'suplier': suplier, 'form': form}
    return TemplateResponse(request, 'dashboard/suplier/form.html', ctx)


@staff_member_required
def suplier_edit(request, pk):
    suplier = get_object_or_404(ProductSuplier, pk=pk)
    form = forms.SuplierForm(request.POST or None, instance=suplier)
    if form.is_valid():
        suplier = form.save()
        msg = pgettext_lazy('Sale (discount) message', 'Обновил поставщика')
        messages.success(request, msg)
        return redirect('dashboard:suplier-update', pk=suplier.pk)
    ctx = {'suplier': suplier, 'form': form}
    return TemplateResponse(request, 'dashboard/suplier/form.html', ctx)


@staff_member_required
def suplier_delete(request, pk):
    instance = get_object_or_404(ProductSuplier, pk=pk)
    if request.method == 'POST':
        instance.delete()
        msg = pgettext_lazy(
            'Sale (discount) message', 'Удален %s') % (instance.name,)
        messages.success(request, msg)
        return redirect('dashboard:suplier-list')
    ctx = {'suplier': instance}
    return TemplateResponse(
        request, 'dashboard/suplier/modal/confirm_delete.html', ctx)


