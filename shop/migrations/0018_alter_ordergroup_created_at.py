# Generated by Django 5.1.3 on 2024-12-16 20:25

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_ordergroup_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergroup',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]