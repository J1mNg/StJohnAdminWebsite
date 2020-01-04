# Generated by Django 3.0.1 on 2020-01-01 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CadetApp', '0010_auto_20191230_1243'),
        ('RewardApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='reward',
            name='required_points',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='reward',
            name='reward_band',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='reward',
            name='source',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.CreateModel(
            name='User_Reward_Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reward_claim_date', models.DateField(null=True)),
                ('cadet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CadetApp.Cadet')),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RewardApp.Reward')),
            ],
        ),
    ]