# Generated by Django 2.2.9 on 2020-02-19 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20200219_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='served_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
