from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import pgettext, ugettext_lazy as _
from django.views.decorators.http import require_POST
from .tokens import account_activation_token
from ..checkout.utils import find_and_assign_anonymous_cart
from ..core.utils import get_paginator_items
from .emails import send_account_delete_confirmation_email, send_account_create_confirmation_email
from .forms import (
    ChangePasswordForm, LoginForm, PasswordResetForm, SignupForm,
    get_address_form, logout_on_password_change, CustomerForm)
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.models import Site
from .models import User
@find_and_assign_anonymous_cart()
def login(request):
    kwargs = {
        'template_name': 'account/login.html',
        'authentication_form': LoginForm}
    return django_views.LoginView.as_view(**kwargs)(request, **kwargs)


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, _('Вы успешно вышли.'))
    return redirect(settings.LOGIN_REDIRECT_URL)


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = auth.authenticate(request=request, email=email, password=password)
        user.is_active = False
        user.save()
        
        site = Site.objects.get_current()
        mail_subject = 'Активируйте ваш аккаунт на BlitzShop'
        message = render_to_string('templated_email/compiled/account_create.html', {
                'domain': site.domain,
                'site_name': site.name,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
        to_email = email
        
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        """send_account_create_confirmation_email.delay(
            account_activation_token.make_token(user), 
            user.email, urlsafe_base64_encode(force_bytes(user.pk)).decode())"""
        messages.success(
            request, pgettext(
                'Storefront message, when user requested his account removed',
                'Проверьте свою почту для подтверждения аккаунта.'))
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    ctx = {'form': form}
    return TemplateResponse(request, 'account/signup.html', ctx)

def account_create_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True;
        user.save()
        
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        msg = pgettext(
            'Ваш аккаунт был успешно подтвержден. ',
            'Ваш аккаунт был успешно подтвержден. В случае каких-либо вопросов свяжитесь с нами.')
        messages.success(request, msg)
        return redirect('/')
    return TemplateResponse(
        request, 'account/signup.html')


def password_reset(request):
    kwargs = {
        'template_name': 'account/password_reset.html',
        'success_url': reverse_lazy('account:reset-password-done'),
        'form_class': PasswordResetForm}
    return django_views.PasswordResetView.as_view(**kwargs)(request, **kwargs)


class PasswordResetConfirm(django_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_from_key.html'
    success_url = reverse_lazy('account:reset-password-complete')
    token = None
    uidb64 = None


def password_reset_confirm(request, uidb64=None, token=None):
    kwargs = {
        'template_name': 'account/password_reset_from_key.html',
        'success_url': reverse_lazy('account:reset-password-complete'),
        'token': token,
        'uidb64': uidb64}
    return PasswordResetConfirm.as_view(**kwargs)(request, **kwargs)


@login_required
def details(request):
    password_form = get_or_process_password_form(request)
    orders = request.user.orders.confirmed().prefetch_related('lines')
    orders_paginated = get_paginator_items(
        orders, settings.PAGINATE_BY, request.GET.get('page'))
    ctx = {'addresses': request.user.addresses.all(),
           'orders': orders_paginated,
           'change_password_form': password_form}

    return TemplateResponse(request, 'account/details.html', ctx)


def get_or_process_password_form(request):
    form = ChangePasswordForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        logout_on_password_change(request, form.user)
        messages.success(request, pgettext(
            'Storefront message', 'Пароль успешно изменен.'))
    return form


@login_required
def address_edit(request, pk):
    """address = get_object_or_404(request.user.addresses, pk=pk)
    address_form, preview = get_address_form(
        request.POST or None, instance=address,
        country_code=address.country.code)
    if address_form.is_valid() and not preview:
        address_form.save()
        message = pgettext(
            'Storefront message', 'Address successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('account:details') + '#addresses')
    return TemplateResponse(
        request, 'account/address_edit.html',
        {'address_form': address_form})"""

    customer = get_object_or_404(User, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        msg = pgettext(
            'Dashboard message', 'Ваши данные успешно обновлены.') 
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('account:details') + '#addresses')
    ctx = {'form': form, 'customer': customer}
    return TemplateResponse(request, 'account/address_edit.html', ctx)

@login_required
def address_delete(request, pk):
    address = get_object_or_404(request.user.addresses, pk=pk)
    if request.method == 'POST':
        address.delete()
        messages.success(
            request,
            pgettext('Storefront message', 'Address successfully removed'))
        return HttpResponseRedirect(reverse('account:details') + '#addresses')
    return TemplateResponse(
        request, 'account/address_delete.html', {'address': address})


@login_required
@require_POST
def account_delete(request):
    user = request.user
    send_account_delete_confirmation_email(str(user.token), user.email)
    messages.success(
        request, pgettext(
            'Storefront message, when user requested his account removed',
            'Проверьте свою почту для подтверждения.'))
    return HttpResponseRedirect(reverse('account:details') + '#settings')


@login_required
def account_delete_confirm(request, token):
    user = request.user

    if str(request.user.token) != token:
        raise Http404('No such page!')

    if request.method == 'POST':
        user.delete()
        msg = pgettext(
            'Ваш аккаунт был успешно удален. '
            'В случае каких-либо вопросов свяжитесь с нами.')
        messages.success(request, msg)
        return redirect('home')

    return TemplateResponse(
        request, 'account/account_delete_prompt.html')
