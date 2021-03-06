from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth import forms as django_forms, update_session_auth_hash
from django.utils.translation import pgettext, pgettext_lazy
from phonenumbers.phonenumberutil import country_code_for_region

from phonenumber_field.formfields import PhoneNumberField
from . import emails
from ..account.models import User
from .i18n import AddressMetaForm, get_address_form_class
from .widgets import PhonePrefixWidget
from .validators import validate_possible_number

class PossiblePhoneNumberFormField(PhoneNumberField):
    """A PhoneNumberField that allows phone numbers from other countries."""

    default_validators = [validate_possible_number]

    def to_python(self, value):
        return value

class FormWithReCaptcha(forms.BaseForm):
    def __new__(cls, *args, **kwargs):
        if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY:
            # insert a Google reCaptcha field inside the form
            # note: label is empty, the reCaptcha is self-explanatory making
            #       the form simpler for the user.
            cls.base_fields['_captcha'] = ReCaptchaField(label='')
        return super(FormWithReCaptcha, cls).__new__(cls)


def get_address_form(data, country_code, initial=None, instance=None, **kwargs):
    country_form = AddressMetaForm(data, initial=initial)
    preview = False
    if country_form.is_valid():
        country_code = country_form.cleaned_data['country']
        preview = country_form.cleaned_data['preview']

    if initial is None and country_code:
        initial = {}
    if country_code:
        initial['phone'] = '+{}'.format(country_code_for_region(country_code))

    address_form_class = get_address_form_class(country_code)

    if not preview and instance is not None:
        address_form_class = get_address_form_class(instance.country.code)
        address_form = address_form_class(data, instance=instance, **kwargs)
    else:
        initial_address = (
            initial if not preview
            else data.dict() if data is not None else data)
        address_form = address_form_class(
            not preview and data or None,
            initial=initial_address,
            **kwargs)
    return address_form, preview


class ChangePasswordForm(django_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].user = self.user
        self.fields['old_password'].widget.attrs['placeholder'] = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = ''
        del self.fields['new_password2']


def logout_on_password_change(request, user):
    if (update_session_auth_hash is not None and
            not settings.LOGOUT_ON_PASSWORD_CHANGE):
        update_session_auth_hash(request, user)


class LoginForm(django_forms.AuthenticationForm, FormWithReCaptcha):
    username = forms.EmailField(
        label=pgettext('Form field', 'Email'), max_length=75)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        if request:
            email = request.GET.get('email')
            if email:
                self.fields['username'].initial = email


class SignupForm(forms.ModelForm, FormWithReCaptcha):
    password = forms.CharField(label='Пароль',
        widget=forms.PasswordInput)
    email = forms.EmailField(
        error_messages={
            'unique': pgettext_lazy(
                'Registration error',
                'Данный email уже занят.')})
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    phone = PossiblePhoneNumberFormField(
        widget=PhonePrefixWidget, required=True, label='Телефон')
    

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
        labels = {
            'email': pgettext_lazy(
                'Email', 'Email'),
            'password': pgettext_lazy(
                'Пароль', 'Пароль'),
            'first_name': pgettext_lazy(
                'Имя', 'Имя'),
            'last_name': pgettext_lazy(
                'Фамилия', 'Фамилия'),
            'phone': pgettext_lazy(
                'Телефон', 'Телефон')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {'autofocus': ''})

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.set_password(password)
        if commit:
            user.save()
        return user

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # disable 'is_active' checkbox if user edits his own account

    class Meta:
        model = User
        fields = ['first_name','last_name','phone','delivery_address']
        labels = {
            'first_name': pgettext_lazy('Customer note', 'Имя'),
            'last_name': pgettext_lazy('Allo', 'Фамилия'),
            'phone': pgettext_lazy('Allo', 'Телефон'),
            'delivery_address': pgettext_lazy('Allo', 'Адрес доставки')}

class PasswordResetForm(django_forms.PasswordResetForm, FormWithReCaptcha):
    """Allow resetting passwords.

    This subclass overrides sending emails to use templated email.
    """

    def get_users(self, email):
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return active_users

    def send_mail(
            self, subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=None):
        # Passing the user object to the Celery task throws an
        # error "'User' is not JSON serializable". Since it's not used in our
        # template, we remove it from the context.
        del context['user']
        emails.send_password_reset_email.delay(context, to_email)
