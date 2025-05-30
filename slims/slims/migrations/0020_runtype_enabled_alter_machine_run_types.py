# Generated by Django 5.1.6 on 2025-04-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0019_lanedata_data_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='runtype',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='run_types',
            field=models.ManyToManyField(related_name='machines', to='slims.runtype'),
        ),
    ]
