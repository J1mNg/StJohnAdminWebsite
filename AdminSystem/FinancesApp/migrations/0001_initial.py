# Generated by Django 2.2.5 on 2019-12-30 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CadetApp', '0010_auto_20191230_1243'),
        ('RollMarkingApp', '0005_auto_20191229_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermFees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('cadet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CadetApp.Cadet')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RollMarkingApp.Meeting')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('details', models.TextField(max_length=100)),
                ('cadet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CadetApp.Cadet')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RollMarkingApp.Meeting')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]