# Generated by Django 2.0.3 on 2018-07-27 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import saleor.account.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(default='', max_length=256)),
                ('last_name', models.CharField(default='', max_length=256)),
                ('phone', saleor.account.models.PossiblePhoneNumberField(blank=True, default='', max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('token', models.UUIDField(default=saleor.account.models.get_token, editable=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'permissions': (('view_user', 'Может просматривать пользователей'), ('edit_user', 'Может редактировать пользователей'), ('view_staff', 'Может смотреть админов'), ('edit_staff', 'Может изменять админов'), ('impersonate_user', 'Может заходить от лица других пользователей')),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=256)),
                ('last_name', models.CharField(default='', max_length=256)),
                ('company_name', models.CharField(default='', max_length=256)),
                ('street_address_1', models.CharField(default='', max_length=256)),
                ('street_address_2', models.CharField(default='', max_length=256)),
                ('city', models.CharField(default='', max_length=256)),
                ('city_area', models.CharField(default='', max_length=128)),
                ('postal_code', models.CharField(default='', max_length=20)),
                ('country', django_countries.fields.CountryField(default='Russian Federation', max_length=2)),
                ('country_area', models.CharField(default='', max_length=128)),
                ('phone', saleor.account.models.PossiblePhoneNumberField(blank=True, default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('content', models.TextField()),
                ('is_public', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='addresses',
            field=models.ManyToManyField(blank=True, related_name='user_addresses', to='account.Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='default_billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='default_shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
