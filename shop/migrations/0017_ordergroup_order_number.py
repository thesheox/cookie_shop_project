# Generated by Django 5.1.3 on 2024-12-16 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergroup',
            name='order_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
