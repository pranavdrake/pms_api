# Generated by Django 3.2.5 on 2023-01-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0038_alter_ratecard_kg_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratecard',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10),
        ),
    ]
