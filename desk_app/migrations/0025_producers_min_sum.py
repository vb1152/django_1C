# Generated by Django 3.1.5 on 2021-10-08 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0024_foldersforfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='producers',
            name='min_sum',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]