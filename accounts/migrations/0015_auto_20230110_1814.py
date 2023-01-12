# Generated by Django 3.2.5 on 2023-01-10 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0025_auto_20230110_1814'),
        ('accounts', '0014_auto_20230107_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvisadetail',
            name='reservation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reservations.reservation'),
        ),
        migrations.AddField(
            model_name='visadetail',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visa_details', to='reservations.reservation'),
        ),
        migrations.AlterField(
            model_name='booker',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='booker',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='booker',
            name='postal_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbooker',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbooker',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalbooker',
            name='postal_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
