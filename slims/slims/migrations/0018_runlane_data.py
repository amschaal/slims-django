# Generated by Django 5.1.6 on 2025-04-17 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0017_alter_lanedata_data_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='runlane',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]
