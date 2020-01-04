# Generated by Django 3.0.1 on 2020-01-01 03:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RewardApp', '0006_auto_20200101_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]