# Generated by Django 3.1.5 on 2021-09-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0021_auto_20210805_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='producers',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
