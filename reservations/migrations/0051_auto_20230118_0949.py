# Generated by Django 3.2.5 on 2023-01-18 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0050_auto_20230117_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltax',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tax',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
