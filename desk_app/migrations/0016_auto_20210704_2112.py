# Generated by Django 3.1.5 on 2021-07-04 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0015_icgroupsmptt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='icgroupsmptt',
            old_name='parent_guid',
            new_name='parent',
        ),
    ]