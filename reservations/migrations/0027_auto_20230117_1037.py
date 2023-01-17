# Generated by Django 3.2.5 on 2023-01-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0026_groupreservation_block_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupreservation',
            name='block_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='groupreservation',
            name='origin',
            field=models.CharField(choices=[('Phone', 'Phone'), ('Walk-in', 'Walk-in'), ('House use', 'House use'), ('Hotel Reservation Office', 'Hotel Reservation Office'), ('EMAIL', 'EMAIL'), ('ONLINE', 'ONLINE')], max_length=100),
        ),
        migrations.AlterField(
            model_name='groupreservation',
            name='status',
            field=models.CharField(choices=[('Enquiry', 'Enquiry'), ('Tentative', 'Tentative'), ('Definite', 'Definite')], max_length=10),
        ),
        migrations.AlterField(
            model_name='groupreservation',
            name='total_rooms',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
