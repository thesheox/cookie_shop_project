# Generated by Django 5.1.4 on 2024-12-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_profile_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
