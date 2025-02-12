# Generated by Django 4.2.18 on 2025-02-11 22:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expiration_month',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
