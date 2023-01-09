# Generated by Django 3.2.5 on 2023-01-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0023_auto_20230109_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalroom',
            name='front_office_status',
            field=models.CharField(choices=[('Vacant', 'Vacant'), ('Occupied', 'Occupied')], max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalroom',
            name='reservation_status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Departed', 'Departed'), ('Stay Over', 'Stay Over'), ('Arrivals', 'Arrivals'), ('Not Reserved', 'Not Reserved'), ('Arrived', 'Arrived'), ('Due Out', 'Due Out'), ('Due Out / Arrivals', 'Due Out / Arrivals')], max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalroom',
            name='room_status',
            field=models.CharField(choices=[('Clean', 'Clean'), ('Inspected', 'Inspected'), ('Dirty', 'Dirty'), ('Out of Order', 'Out of Order'), ('Out of Service', 'Out of Service')], max_length=100),
        ),
        migrations.AlterField(
            model_name='room',
            name='front_office_status',
            field=models.CharField(choices=[('Vacant', 'Vacant'), ('Occupied', 'Occupied')], max_length=100),
        ),
        migrations.AlterField(
            model_name='room',
            name='reservation_status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Departed', 'Departed'), ('Stay Over', 'Stay Over'), ('Arrivals', 'Arrivals'), ('Not Reserved', 'Not Reserved'), ('Arrived', 'Arrived'), ('Due Out', 'Due Out'), ('Due Out / Arrivals', 'Due Out / Arrivals')], max_length=100),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_status',
            field=models.CharField(choices=[('Clean', 'Clean'), ('Inspected', 'Inspected'), ('Dirty', 'Dirty'), ('Out of Order', 'Out of Order'), ('Out of Service', 'Out of Service')], max_length=100),
        ),
    ]
