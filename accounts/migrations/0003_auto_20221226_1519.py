# Generated by Django 3.2.5 on 2022-12-26 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0002_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='Department',
        ),
        migrations.AlterModelOptions(
            name='department',
            options={},
        ),
    ]