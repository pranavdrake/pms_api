# Generated by Django 3.2.5 on 2023-01-11 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0028_auto_20230111_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subgroup',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_groups', to='reservations.group'),
        ),
    ]
