# Generated by Django 4.2.18 on 2025-01-31 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_address_alter_base_base_alter_base_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
