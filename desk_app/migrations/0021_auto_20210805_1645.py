# Generated by Django 3.1.5 on 2021-08-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0020_prices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ic_scu',
            name='scu_barcode',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
