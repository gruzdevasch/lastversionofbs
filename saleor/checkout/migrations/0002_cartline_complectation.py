# Generated by Django 2.0.3 on 2018-08-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartline',
            name='complectation',
            field=models.TextField(blank=True, null=True),
        ),
    ]