# Generated by Django 4.2.18 on 2025-01-28 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('zip', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=9, null=True)),
                ('organization', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'address',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BioshareShare',
            fields=[
                ('share_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('project_id', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'bioshare_share',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ConfigFile',
            fields=[
                ('config_file_id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('file_path', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('output_dir', models.CharField(blank=True, max_length=250, null=True)),
                ('file_contents', models.TextField(blank=True, null=True)),
                ('has_run', models.IntegerField(blank=True, null=True)),
                ('post_run_command', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'db_table': 'config_file',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ConfigFileRun',
            fields=[
                ('config_file_run_id', models.AutoField(primary_key=True, serialize=False)),
                ('firecrest', models.CharField(blank=True, max_length=50, null=True)),
                ('bustard', models.CharField(blank=True, max_length=50, null=True)),
                ('out_dir', models.CharField(blank=True, max_length=50, null=True)),
                ('make_date', models.DateField(blank=True, null=True)),
                ('make_creator', models.CharField(blank=True, max_length=25, null=True)),
                ('run_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'db_table': 'config_file_run',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('confirmation_id', models.AutoField(primary_key=True, serialize=False)),
                ('confid', models.CharField(db_column='confID', max_length=32)),
                ('confirmed', models.IntegerField()),
            ],
            options={
                'db_table': 'confirmation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DbGroup',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('db_group', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('share_id', models.CharField(blank=True, max_length=15, null=True)),
                ('bioshare_group_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'db_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MaqgeneLanes',
            fields=[
                ('maqgene_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('run_lane_id', models.IntegerField()),
            ],
            options={
                'db_table': 'maqgene_lanes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('organism_id', models.AutoField(primary_key=True, serialize=False)),
                ('organism', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('genome_file', models.CharField(blank=True, db_column='GENOME_FILE', max_length=250, null=True)),
                ('genome_dir', models.CharField(blank=True, db_column='GENOME_DIR', max_length=250, null=True)),
            ],
            options={
                'db_table': 'organism',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('permission', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('phone_id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(blank=True, max_length=25, null=True)),
                ('type', models.CharField(blank=True, max_length=9, null=True)),
            ],
            options={
                'db_table': 'phone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pwdrecover',
            fields=[
                ('pwdrecover_id', models.AutoField(primary_key=True, serialize=False)),
                ('recoverid', models.CharField(db_column='recoverID', max_length=32)),
            ],
            options={
                'db_table': 'pwdrecover',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('role_permission_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'role_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('run_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('submitted', models.DateTimeField(blank=True, null=True)),
                ('num_cycles', models.IntegerField(blank=True, null=True)),
                ('run_date', models.DateField(blank=True, null=True)),
                ('machine', models.CharField(blank=True, max_length=100, null=True)),
                ('run_dir', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('pipeline', models.IntegerField(blank=True, null=True)),
                ('request_transfer', models.IntegerField(blank=True, null=True)),
                ('last_transfer', models.DateTimeField(blank=True, null=True)),
                ('run_type', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'run',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RunEmail',
            fields=[
                ('email_id', models.AutoField(primary_key=True, serialize=False)),
                ('run_id', models.IntegerField()),
                ('group_id', models.IntegerField()),
                ('status', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('sent_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'run_email',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RunLane',
            fields=[
                ('run_lane_id', models.AutoField(primary_key=True, serialize=False)),
                ('lane_number', models.CharField(blank=True, max_length=2, null=True)),
                ('concentration', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('random_dir', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('delete_analysis_permitted', models.DateTimeField(blank=True, null=True)),
                ('delete_images_permitted', models.DateTimeField(blank=True, null=True)),
                ('images_deleted_by', models.IntegerField(blank=True, null=True)),
                ('analysis_deleted_by', models.IntegerField(blank=True, null=True)),
                ('lane_dir', models.CharField(blank=True, max_length=40, null=True)),
                ('job_id', models.CharField(blank=True, max_length=50, null=True)),
                ('project_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'run_lane',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysRuns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_name', models.CharField(blank=True, max_length=150, null=True)),
                ('run_date', models.CharField(blank=True, max_length=50, null=True)),
                ('directory', models.CharField(blank=True, max_length=255, null=True)),
                ('date_discovered', models.DateTimeField(blank=True, null=True)),
                ('date_last_sync', models.DateTimeField(blank=True, null=True)),
                ('size_on_host_kb', models.PositiveBigIntegerField(blank=True, null=True)),
                ('solexa_server', models.CharField(blank=True, max_length=100, null=True)),
                ('host_server', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('date_last_check', models.DateTimeField(blank=True, null=True)),
                ('image_server', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'sys_runs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_server', models.CharField(blank=True, max_length=100, null=True)),
                ('file_system', models.CharField(blank=True, max_length=255, null=True)),
                ('mount_point', models.CharField(blank=True, max_length=255, null=True)),
                ('space_used_kb', models.PositiveBigIntegerField(blank=True, null=True)),
                ('space_total_kb', models.PositiveBigIntegerField(blank=True, null=True)),
                ('space_avail_kb', models.PositiveBigIntegerField(blank=True, null=True)),
                ('percent_used', models.PositiveIntegerField(blank=True, null=True)),
                ('date_last_check', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sys_space',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(blank=True, max_length=60, null=True)),
                ('password', models.CharField(blank=True, max_length=32, null=True)),
                ('firstname', models.CharField(blank=True, max_length=30, null=True)),
                ('lastname', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserGroupPermission',
            fields=[
                ('user_group_permission_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_group_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserGroupRole',
            fields=[
                ('user_group_role_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_group_role',
                'managed': False,
            },
        ),
    ]
