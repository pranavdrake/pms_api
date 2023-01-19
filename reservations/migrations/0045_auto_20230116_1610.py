# Generated by Django 3.2.5 on 2023-01-16 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0044_auto_20230116_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreservation',
            name='reservation_status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('Wait-list', 'Wait-list'), ('Due In', 'Due In'), ('Checked In', 'Checked In'), ('Due Out', 'Due Out'), ('Roll Over', 'Roll Over'), ('Checked Out', 'Checked Out'), ('No Show', 'No Show'), ('Cancelled', 'Cancelled'), ('Not Reserved', 'Not Reserved'), ('Enquiry Only', 'Enquiry Only')], max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='stay_total',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_base_amount',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_cost_of_stay',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_discount',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_extra_charge',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_payment',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='total_tax',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='travel_agent_commission',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('Wait-list', 'Wait-list'), ('Due In', 'Due In'), ('Checked In', 'Checked In'), ('Due Out', 'Due Out'), ('Roll Over', 'Roll Over'), ('Checked Out', 'Checked Out'), ('No Show', 'No Show'), ('Cancelled', 'Cancelled'), ('Not Reserved', 'Not Reserved'), ('Enquiry Only', 'Enquiry Only')], max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='stay_total',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_base_amount',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_cost_of_stay',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_discount',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_extra_charge',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_payment',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_tax',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='travel_agent_commission',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]