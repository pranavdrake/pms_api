# Generated by Django 3.2.5 on 2023-02-03 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_alter_dailydetail_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalroommove',
            name='reservation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reservations.reservation'),
        ),
        migrations.AddField(
            model_name='roommove',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_moves', to='reservations.reservation'),
        ),
        migrations.AlterField(
            model_name='dailydetail',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_details', to='reservations.reservation'),
        ),
    ]
