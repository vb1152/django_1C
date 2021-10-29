# Generated by Django 3.1.5 on 2021-07-04 17:55

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('desk_app', '0014_delete_icgroupsmptt'),
    ]

    operations = [
        migrations.CreateModel(
            name='ICgroupsMPTT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=70)),
                ('group_code', models.CharField(max_length=9)),
                ('group_guid', models.CharField(max_length=36, unique=True)),
                ('parent_guid_str', models.CharField(default='str', max_length=36)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent_guid', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='desk_app.icgroupsmptt')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]