# Generated by Django 3.2.5 on 2023-02-01 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0002_auto_20230130_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSplitTransaction',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('split_by', models.CharField(choices=[('Amount', 'Amount'), ('Percentage', 'Percentage')], max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('split_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('split_amount_with_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reservations.transaction')),
            ],
            options={
                'verbose_name': 'historical split transaction',
                'verbose_name_plural': 'historical split transactions',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='SplitTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('split_by', models.CharField(choices=[('Amount', 'Amount'), ('Percentage', 'Percentage')], max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('split_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('split_amount_with_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='split_transactions', to='reservations.transaction')),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='images',
        ),
        migrations.AddField(
            model_name='document',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_images', to='reservations.room'),
        ),
        migrations.AddField(
            model_name='historicaldocument',
            name='room',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reservations.room'),
        ),
        migrations.AlterField(
            model_name='document',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='reservations.reservation'),
        ),
        migrations.DeleteModel(
            name='HistoricalRoomImage',
        ),
        migrations.DeleteModel(
            name='RoomImage',
        ),
    ]
