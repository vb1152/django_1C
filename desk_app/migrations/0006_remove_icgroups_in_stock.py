# Generated by Django 3.1.5 on 2021-06-30 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0005_icgroups_in_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icgroups',
            name='in_stock',
        ),
    ]