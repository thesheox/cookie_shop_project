# Generated by Django 5.1.3 on 2024-12-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_ordergroup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergroup',
            name='delivery_method',
            field=models.CharField(choices=[('دریافت حضوری', 'دریافت حضوری'), ('ارسال با پیک', 'ارسال با پیک')], default='دریافت حضوری', max_length=50),
        ),
    ]
