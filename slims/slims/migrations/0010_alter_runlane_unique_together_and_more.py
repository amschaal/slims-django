# Generated by Django 4.2.18 on 2025-02-21 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreomics', '0004_alter_submission_options'),
        ('slims', '0009_runlane_submission'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='runlane',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='runlane',
            name='submission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='lanes', to='coreomics.submission'),
        ),
    ]
