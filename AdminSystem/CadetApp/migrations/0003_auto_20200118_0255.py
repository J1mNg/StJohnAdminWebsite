# Generated by Django 3.0.1 on 2020-01-18 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CadetApp', '0002_cadet_dems_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadet',
            name='meeting_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='cadet',
            name='other_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='cadet',
            name='total_duty_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='cadet',
            name='training_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
