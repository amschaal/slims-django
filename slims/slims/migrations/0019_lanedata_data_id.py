# Generated by Django 5.1.6 on 2025-04-18 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0018_runlane_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='lanedata',
            name='data_id',
            field=models.SlugField(null=True),
        ),
    ]
