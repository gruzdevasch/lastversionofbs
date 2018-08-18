from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from templated_email import send_templated_mail
from django.template.loader import render_to_string
from ..core.utils import build_absolute_uri
from django.template import RequestContext
from django.core.mail import EmailMessage

@shared_task
def send_password_reset_email(context, recipient):
    reset_url = build_absolute_uri(
        reverse(
            'account:reset-password-confirm',
            kwargs={'uidb64': context['uid'], 'token': context['token']}))
    context['reset_url'] = reset_url
    send_templated_mail(
        template_name='account/password_reset',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        context=context)

@shared_task
def send_account_create_confirmation_email(token, recipient_email, uid):
    site = Site.objects.get_current()
    delete_url = build_absolute_uri(
        reverse('account:account-create-confirmation', kwargs={'uidb64':uid, 'token': token}))
    ctx = {'site_name': site.name, 'domain': site.domain, 'url': delete_url}
    send_templated_mail(
        template_name='account/account_create',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        context=ctx)
		
@shared_task
def send_account_delete_confirmation_email(token, recipient_email):
    site = Site.objects.get_current()
    delete_url = build_absolute_uri(
        reverse('account:delete-confirm', kwargs={'token': token}))
    ctx = {'site_name': site.name, 'domain': site.domain, 'url': delete_url}
    send_templated_mail(
        template_name='account/account_delete',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        context=ctx)
