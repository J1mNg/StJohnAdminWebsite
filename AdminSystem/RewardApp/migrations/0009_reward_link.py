# Generated by Django 3.0.1 on 2020-01-01 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RewardApp', '0008_auto_20200101_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='link',
            field=models.CharField(default='Not Applicable', max_length=100),
        ),
    ]
