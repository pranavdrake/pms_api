# Generated by Django 3.2.5 on 2023-01-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0031_historicaltax'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_duplicate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_moved',
            field=models.BooleanField(default=False),
        ),
    ]
