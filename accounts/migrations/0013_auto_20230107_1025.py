# Generated by Django 3.2.5 on 2023-01-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_booker_historicalbooker_historicaliddetails_historicalmembershiplevel_historicalmembershiptype_histo'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvisadetails',
            name='visa_file',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='visadetails',
            name='visa_file',
            field=models.FileField(null=True, upload_to='visa_files/'),
        ),
        migrations.AlterField(
            model_name='historicaliddetails',
            name='id_file',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='iddetails',
            name='id_file',
            field=models.FileField(null=True, upload_to='guest_ids/'),
        ),
    ]
