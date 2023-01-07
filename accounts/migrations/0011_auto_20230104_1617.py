# Generated by Django 3.2.5 on 2023-01-04 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_account_guestprofile_historicalaccount_historicalcustomuser_historicaldepartment_historicalguestprof'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestprofile',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalguestprofile',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='IDDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('id_type', models.CharField(choices=[('A', 'Adhaar'), ('P', 'Passport'), ('PN', 'Pan')], max_length=10)),
                ('issue_place', models.CharField(max_length=100)),
                ('id_file', models.FileField(upload_to='guest_ids/')),
                ('id_number', models.CharField(max_length=100)),
                ('issue_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_details', to='accounts.guestprofile')),
            ],
        ),
    ]