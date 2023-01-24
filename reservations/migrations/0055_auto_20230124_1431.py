# Generated by Django 3.2.5 on 2023-01-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0054_alter_folio_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpickupdropdetails',
            name='carrier_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpickupdropdetails',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpickupdropdetails',
            name='station_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpickupdropdetails',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpickupdropdetails',
            name='transport_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupdropdetails',
            name='carrier_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupdropdetails',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pickupdropdetails',
            name='station_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupdropdetails',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pickupdropdetails',
            name='transport_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
