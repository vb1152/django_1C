# Generated by Django 3.1.5 on 2021-06-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desk_app', '0003_auto_20210628_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataForProgressbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('count', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
    ]
