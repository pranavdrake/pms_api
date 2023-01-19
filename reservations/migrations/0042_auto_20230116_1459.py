# Generated by Django 3.2.5 on 2023-01-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0041_alter_paymenttype_transaction_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreservation',
            name='origin',
            field=models.CharField(choices=[('Phone', 'Phone'), ('Walk-in', 'Walk-in'), ('House use', 'House use'), ('Hotel Reservation Office', 'Hotel Reservation Office'), ('EMAIL', 'EMAIL'), ('ONLINE', 'ONLINE')], max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalreservation',
            name='reservation_status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('Wait-list', 'Wait-list'), ('Due In', 'Due In'), ('Checked In', 'Checked In'), ('Due Out', 'Due Out'), ('Roll Over', 'Roll Over'), ('Checked Out', 'Checked Out'), ('No Show', 'No Show'), ('CAN', 'Cancelled'), ('Not Reserved', 'Not Reserved'), ('Enquiry Only', 'Enquiry Only')], max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='origin',
            field=models.CharField(choices=[('Phone', 'Phone'), ('Walk-in', 'Walk-in'), ('House use', 'House use'), ('Hotel Reservation Office', 'Hotel Reservation Office'), ('EMAIL', 'EMAIL'), ('ONLINE', 'ONLINE')], max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('Wait-list', 'Wait-list'), ('Due In', 'Due In'), ('Checked In', 'Checked In'), ('Due Out', 'Due Out'), ('Roll Over', 'Roll Over'), ('Checked Out', 'Checked Out'), ('No Show', 'No Show'), ('CAN', 'Cancelled'), ('Not Reserved', 'Not Reserved'), ('Enquiry Only', 'Enquiry Only')], max_length=100),
        ),
    ]