# Generated by Django 2.2.9 on 2020-02-19 06:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20200218_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='served_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
