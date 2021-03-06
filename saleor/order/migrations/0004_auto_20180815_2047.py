# Generated by Django 2.0.3 on 2018-08-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderline_complectation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fulfillment',
            name='status',
            field=models.CharField(choices=[('fulfilled', 'Обработан'), ('canceled', 'Отменен')], default='fulfilled', max_length=32),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('paid', 'В обработке'), ('delivered', 'Доставлен'), ('unfulfilled', 'Не обработан'), ('partially fulfilled', 'Частично обработан'), ('fulfilled', 'Обработан'), ('canceled', 'Отменен')], default='unfulfilled', max_length=32),
        ),
        migrations.AlterField(
            model_name='suplierorder',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('paid', 'В обработке'), ('delivered', 'Доставлен'), ('unfulfilled', 'Не обработан'), ('partially fulfilled', 'Частично обработан'), ('fulfilled', 'Обработан'), ('canceled', 'Отменен')], default='current', max_length=32),
        ),
    ]
