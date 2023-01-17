# Generated by Django 3.2.5 on 2023-01-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20230110_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestprofile',
            name='guest_status',
            field=models.CharField(choices=[('In House', 'In House'), ('Out', 'Out')], default='Out', max_length=255),
        ),
        migrations.AddField(
            model_name='historicalguestprofile',
            name='guest_status',
            field=models.CharField(choices=[('In House', 'In House'), ('Out', 'Out')], default='Out', max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Company', 'Company'), ('Travel Agent', 'Travel Agent'), ('Group', 'Group')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='salutation',
            field=models.CharField(choices=[('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Capt', 'Capt'), ('Wg Cdr', 'Wg Cdr'), ('Major', 'Major'), ('Colonel', 'Colonel')], max_length=10),
        ),
        migrations.AlterField(
            model_name='historicalaccount',
            name='account_type',
            field=models.CharField(choices=[('Company', 'Company'), ('Travel Agent', 'Travel Agent'), ('Group', 'Group')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='historicalguestprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalguestprofile',
            name='salutation',
            field=models.CharField(choices=[('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Capt', 'Capt'), ('Wg Cdr', 'Wg Cdr'), ('Major', 'Major'), ('Colonel', 'Colonel')], max_length=10),
        ),
    ]
