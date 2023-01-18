# Generated by Django 3.2.5 on 2023-01-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20230110_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('company', 'Company'), ('travel_agent', 'Travel Agent'), ('group', 'Group')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='historicalaccount',
            name='account_type',
            field=models.CharField(choices=[('company', 'Company'), ('travel_agent', 'Travel Agent'), ('group', 'Group')], max_length=20, null=True),
        ),
    ]