# Generated by Django 3.2.5 on 2023-01-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0031_auto_20230111_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalratecode',
            name='complementary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalratecode',
            name='house_use',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ratecode',
            name='complementary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ratecode',
            name='house_use',
            field=models.BooleanField(default=False),
        ),
    ]
