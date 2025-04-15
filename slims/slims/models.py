# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

#  Must first run: python manage.py migrate slims --fake-initial
#  Then run: python manage.py migrate slims
from functools import cached_property
import random
import string
import uuid
from django.db import models
from django.contrib.auth.models import Group, User as AuthUser
from django.utils import timezone

from coreomics.models import Submission

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=9, blank=True, null=True)
    organization = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'address'


class BioshareShare(models.Model):
    share_id = models.CharField(primary_key=True, max_length=20)
    run = models.ForeignKey('Run', models.DO_NOTHING)
    project_id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bioshare_share'
        unique_together = (('run', 'project_id'),)


class ConfigFile(models.Model):
    config_file_id = models.AutoField(primary_key=True)
    run = models.ForeignKey('Run', models.DO_NOTHING)
    created = models.DateTimeField(blank=True, null=True)
    file_path = models.CharField(unique=True, max_length=250, blank=True, null=True)
    output_dir = models.CharField(max_length=250, blank=True, null=True)
    file_contents = models.TextField(blank=True, null=True)
    has_run = models.IntegerField(blank=True, null=True)
    post_run_command = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'config_file'


class ConfigFileRun(models.Model):
    config_file_run_id = models.AutoField(primary_key=True)
    config_file = models.ForeignKey(ConfigFile, models.DO_NOTHING)
    firecrest = models.CharField(max_length=50, blank=True, null=True)
    bustard = models.CharField(max_length=50, blank=True, null=True)
    out_dir = models.CharField(max_length=50, blank=True, null=True)
    make_date = models.DateField(blank=True, null=True)
    make_creator = models.CharField(max_length=25, blank=True, null=True)
    run_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'config_file_run'


class Confirmation(models.Model):
    confirmation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    confid = models.CharField(db_column='confID', max_length=32)  # Field name made lowercase.
    confirmed = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'confirmation'


class DbGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    db_group = models.CharField(unique=True, max_length=40, blank=True, null=True)
    share_id = models.CharField(max_length=15, blank=True, null=True)
    bioshare_group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'db_group'


class MaqgeneLanes(models.Model):
    maqgene_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    run_lane_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'maqgene_lanes'


class Organism(models.Model):
    organism_id = models.AutoField(primary_key=True)
    organism = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genome_file = models.CharField(db_column='GENOME_FILE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    genome_dir = models.CharField(db_column='GENOME_DIR', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'organism'


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'permission'


class Phone(models.Model):
    phone_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    number = models.CharField(max_length=25, blank=True, null=True)
    type = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'phone'


class Pwdrecover(models.Model):
    pwdrecover_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    recoverid = models.CharField(db_column='recoverID', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pwdrecover'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'


class RolePermission(models.Model):
    role_permission_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'role_permission'
        unique_together = (('role', 'permission'),)

class RunType(models.Model):
    id = models.SlugField(max_length=20, blank=False, primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    def __str__(self):
        return self.name

class Machine(models.Model):
    id = models.SlugField(max_length=20, blank=False, primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    base_directory = models.CharField(max_length=75, null=True, blank=True)
    run_types = models.ManyToManyField(RunType, symmetrical=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class Run(models.Model):
    type = models.ForeignKey(RunType, null=True, on_delete=models.RESTRICT)
    run_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    submitted = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    num_cycles = models.IntegerField(blank=True, null=True)
    run_date = models.DateField(blank=True, null=True)
    machine = models.ForeignKey(Machine, null=True, on_delete=models.RESTRICT)
    machine_name = models.CharField(max_length=100, blank=True, null=True)
    run_dir = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    pipeline = models.IntegerField(blank=True, null=True)
    request_transfer = models.IntegerField(blank=True, null=True)
    last_transfer = models.DateTimeField(blank=True, null=True)
    run_type = models.CharField(max_length=15, blank=True, null=True)
    def ordered_lanes(self, user=None):
        lanes = self.lanes.all().order_by('lane_number')
        if user and not user.is_staff:
            return lanes.filter(group__in=user.groups.all())
        else:
            return lanes
    @property
    def can_delete(self):
        days_old = (timezone.now() - self.submitted).days
        return days_old < 7
    @property
    def can_modify(self):
        days_old = (timezone.now() - self.submitted).days
        return days_old < 90
    @cached_property
    def run_class(self):
        from .run_type import RunType, RunTypeRegistry
        return RunTypeRegistry.get(self.type_id)(self)
        # return RunTypeRegistry.get(self.run_type)(self)
    def get_machine(self):
        return self.machine_name or self.machine
    def __str__(self):
        return '{}: {}'.format((str(self.run_date) if self.run_date else str(self.submitted)), (self.machine or ''))
    class Meta:
        managed = True
        db_table = 'run'

class RunEmail(models.Model):
    email_id = models.AutoField(primary_key=True)
    run_id = models.IntegerField()
    group_id = models.IntegerField()
    status = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    sent_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'run_email'

def generate_random_string(length=15):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))

class RunLane(models.Model):
    run_lane_id = models.AutoField(primary_key=True)
    run = models.ForeignKey(Run, models.DO_NOTHING, related_name='lanes')
    lane_number = models.CharField(max_length=2, blank=True, null=True)
    # db_group = models.ForeignKey(DbGroup, models.DO_NOTHING)
    group = models.ForeignKey(Group, null=True, on_delete=models.RESTRICT)
    organism = models.ForeignKey(Organism, models.DO_NOTHING, blank=True, null=True)
    concentration = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    random_dir = models.CharField(unique=True, max_length=15, blank=True, null=True)
    delete_analysis_permitted = models.DateTimeField(blank=True, null=True)
    delete_images_permitted = models.DateTimeField(blank=True, null=True)
    images_deleted_by = models.IntegerField(blank=True, null=True)
    analysis_deleted_by = models.IntegerField(blank=True, null=True)
    lane_dir = models.CharField(max_length=40, blank=True, null=True)
    job_id = models.CharField(max_length=50, blank=True, null=True)
    project_id = models.CharField(max_length=50, blank=True, null=True)
    submission = models.ForeignKey(Submission, models.RESTRICT, null=True, related_name='lanes') # fix character sets or do: alter table coreomics_submission convert to character set latin1;
    def generate_data_dirs(self):
        return self.run.run_class.generate_lane_directories(self)
    def __str__(self):
        return '{}'.format(self.lane_number)
    @property
    def data_url(self):
        if self.submission and self.submission.share:
            return self.submission.share.url
        elif self.random_dir:
            return 'http://slimsdata.genomecenter.ucdavis.edu/Data/{}/'.format(self.random_dir)
    @staticmethod
    def get_user_lanes(user):
        return RunLane.objects.filter(group__in=user.groups.all())
    @property
    def pi_name(self):
        if self.submission:
            return self.submission.pi_name
        elif self.group:
            return str(self.group)
        return None
    def grouped_directories(self):
        statuses = {}
        for d in self.directories.all():
            if d.status not in statuses:
                statuses[d.status] = []
            statuses[d.status].append(d)
        return statuses
    # def create_data_dirs(self):
    #     self.directories.exclude(status=LaneData.STATUS_COMPLETE).delete()
    #     directories = self.generate_data_dirs()
    #     instances = [LaneData(lane=self, data_path=d, repository_subpath=d.split('/')[-1]) for d in directories]
    #     return LaneData.objects.bulk_create(instances)
    def save(self, **kwargs):
        status = super().save(**kwargs)
        self.run.run_class.create_lane_directories(self)
        return status
    class Meta:
        managed = True
        db_table = 'run_lane'
        # unique_together = (('run', 'lane_number'),)

class LaneData(models.Model):
    TRANSFER_COPY = 'COPY'
    TRANSFER_LINK = 'LINK'
    TRANSFER_CHOICES = ((TRANSFER_COPY, TRANSFER_COPY), (TRANSFER_LINK, TRANSFER_LINK))
    STATUS_NEW = 'NEW'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_ERROR = 'ERROR'
    STATUS_COMPLETE = 'COMPLETE'
    STATUSES = ((STATUS_NEW, 'New'), (STATUS_IN_PROGRESS, 'Transfer In Progress'), (STATUS_ERROR, 'Error'), (STATUS_COMPLETE, 'Complete'))
    lane = models.ForeignKey(RunLane, related_name='directories', on_delete=models.CASCADE)
    data_path = models.CharField(max_length=100)
    repository_subpath = models.CharField(max_length=100)
    transfer_type = models.CharField(max_length=10, choices=TRANSFER_CHOICES, default=TRANSFER_LINK)
    status = models.CharField(max_length=15, choices=STATUSES, default=STATUS_NEW)
    message = models.TextField(null=True)
    def share(self):
        if not self.can_share:
            return False
        if self.transfer_type == LaneData.TRANSFER_LINK:
            try:
                data = self.lane.submission.share.link(self.data_path, self.repository_subpath)
                if data['status'] == 'success':
                    self.status = LaneData.STATUS_COMPLETE
                    self.message = 'Linking complete'
                else:
                    self.status = LaneData.STATUS_ERROR
                    if 'errors' in data:
                        self.message = str(data['errors'])
            except Exception as e:
                self.status = LaneData.STATUS_ERROR
                self.message = 'There was an error linking: {}'.format(e)
            self.save()
            return True
        return False
    @property
    def can_share(self):
        return self.status in [LaneData.STATUS_NEW, LaneData.STATUS_ERROR]
    @property
    def can_delete(self):
        return self.status in [LaneData.STATUS_NEW, LaneData.STATUS_ERROR]
    @property
    def can_modify(self):
        return self.status in [LaneData.STATUS_NEW, LaneData.STATUS_ERROR]
    def __str__(self):
        return self.data_path

class SysRuns(models.Model):
    run_name = models.CharField(max_length=150, blank=True, null=True)
    run_date = models.CharField(max_length=50, blank=True, null=True)
    directory = models.CharField(max_length=255, blank=True, null=True)
    date_discovered = models.DateTimeField(blank=True, null=True)
    date_last_sync = models.DateTimeField(blank=True, null=True)
    size_on_host_kb = models.PositiveBigIntegerField(blank=True, null=True)
    solexa_server = models.CharField(max_length=100, blank=True, null=True)
    host_server = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    date_last_check = models.DateTimeField(blank=True, null=True)
    image_server = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sys_runs'


class SysSpace(models.Model):
    host_server = models.CharField(max_length=100, blank=True, null=True)
    file_system = models.CharField(max_length=255, blank=True, null=True)
    mount_point = models.CharField(max_length=255, blank=True, null=True)
    space_used_kb = models.PositiveBigIntegerField(blank=True, null=True)
    space_total_kb = models.PositiveBigIntegerField(blank=True, null=True)
    space_avail_kb = models.PositiveBigIntegerField(blank=True, null=True)
    percent_used = models.PositiveIntegerField(blank=True, null=True)
    date_last_check = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sys_space'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'


class UserGroupPermission(models.Model):
    user_group_permission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)
    group = models.ForeignKey(DbGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'user_group_permission'
        unique_together = (('user', 'permission', 'group'),)


class UserGroupRole(models.Model):
    user_group_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    role = models.ForeignKey(Role, models.DO_NOTHING)
    group = models.ForeignKey(DbGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'user_group_role'
        unique_together = (('user', 'role', 'group'),)


def is_pi(self):
    return self.has_perm('auth.is_pi')
AuthUser.is_pi = is_pi