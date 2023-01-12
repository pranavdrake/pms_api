# Generated by Django 3.2.5 on 2023-01-10 16:52

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0029_auto_20230110_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalratecode',
            name='days_applicable',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=56, null=True),
        ),
        migrations.AlterField(
            model_name='ratecode',
            name='days_applicable',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=56, null=True),
        ),
    ]
