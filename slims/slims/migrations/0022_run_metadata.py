# Generated by Django 5.1.6 on 2025-05-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0021_run_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='metadata',
            field=models.JSONField(default=dict),
        ),
    ]
