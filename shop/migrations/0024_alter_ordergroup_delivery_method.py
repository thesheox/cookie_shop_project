# Generated by Django 5.1.3 on 2024-12-27 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_remove_profile_default_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergroup',
            name='delivery_method',
            field=models.CharField(choices=[('pickup', 'Pickup'), ('courier', 'Courier')], default='pickup', max_length=10),
        ),
    ]