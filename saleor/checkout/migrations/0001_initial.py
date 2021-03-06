# Generated by Django 2.0.3 on 2018-07-27 06:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_prices.models
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipping', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('discount_amount', django_prices.models.MoneyField(currency='RUB', decimal_places=2, default=0, max_digits=12)),
                ('discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('voucher_code', models.CharField(blank=True, max_length=12, null=True)),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to='shipping.ShippingMethodCountry')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-last_change',),
            },
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('data', jsonfield.fields.JSONField(blank=True, default={})),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='checkout.Cart')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='product.ProductVariant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together={('cart', 'variant', 'data')},
        ),
    ]
