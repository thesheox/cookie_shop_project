# Generated by Django 5.1.3 on 2024-12-27 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_ordergroup_delivery_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergroup',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='order_images/'),
        ),
    ]