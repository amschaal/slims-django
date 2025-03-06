from django.db import models
from .config import VIEW_URL, GET_PERMISSIONS_URL, SET_PERMISSIONS_URL, FILESYSTEM_ID, DEFAULT_GROUP
from coreomics.models import Submission
from .requests import bioshare_post, bioshare_get, create_share, link_data
from django.utils import timezone

class SubmissionShare(models.Model):
    ADMIN_PERMISSIONS = ["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]
    VIEWER_PERMISSIONS = ["view_share_files","download_share_files"]
    id = models.CharField(max_length=30, primary_key=True)
    submission = models.OneToOneField(Submission, on_delete=models.RESTRICT, related_name='share') # Fix char sets or run: alter table bioshare_submissionshare convert to character set latin1;
    name = models.CharField(max_length=50)
    notes = models.TextField(null=True)
    bioshare_id = models.CharField(max_length=15,null=True,blank=True)
    permissions = models.JSONField(null=True)
    updated = models.DateTimeField(null=True)
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = '{}: {}'.format(self.submission.pi_name,self.submission.internal_id)
        if not self.notes:
            self.notes = 'Generated from {}'.format(self.submission.internal_id)
        if not self.bioshare_id:
            # name = self.name or '{}: {}'.format(self.submission.pi_name,self.submission.internal_id)
            # notes = self.notes or 
            filesystem = FILESYSTEM_ID
            self.bioshare_id = create_share(self.name, self.notes, filesystem)
        if not self.id:
            self.id = '{}_{}'.format(self.submission.pk, self.bioshare_id)
        instance = super(SubmissionShare, self).save(*args, **kwargs)
        # self.share_with_group()
        # self.share_with_participants()
        # self.share_with_group_and_participants()
        return instance
    def __str__(self):
        return self.name
    @property
    def url(self):
        return VIEW_URL.format(id=self.bioshare_id)
    def set_permissions(self, perms=None):
#         if not perms:
#             perms = {"test": True, "groups": {}, "users":dict([(p.email,["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]) for p in self.submission.participants.all()]), "email":True}
#         print('perms', perms)
#       perms = {"users":{"jdoe@domain.com":["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]},"groups":{"1":["view_share_files","download_share_files","write_to_share"]},"email":true}
        perms = bioshare_post(SET_PERMISSIONS_URL.format(id=self.bioshare_id), perms)
        if not self.permissions:
            self.permissions = {}
        self.permissions['user_perms'] = perms['user_perms']
        self.permissions['group_perms'] =  perms['group_perms']
        self.updated = timezone.now()
        self.save(update_fields=['permissions', 'updated'])
    def share_with_participants(self, email=False):
        perms = {"groups": {}, "users":dict([(p.email, self.ADMIN_PERMISSIONS) for p in self.submission.data['participants']]), "email":email}
        return self.set_permissions(perms)
    def share_with_group(self, email=False):
        if DEFAULT_GROUP:
            perms = {"groups": {DEFAULT_GROUP: self.VIEWER_PERMISSIONS}, "email":email}
            return self.set_permissions(perms)
    def share_with_group_and_participants(self, email=False):
        perms = {"groups": {DEFAULT_GROUP: self.VIEWER_PERMISSIONS}, "users":dict([(p['email'], self.ADMIN_PERMISSIONS) for p in self.submission.data['participants']]), "email":email}
        return self.set_permissions(perms)
    def share(self, contacts=True, email=False):
        emails = [self.submission.submitter_email, self.submission.pi_email]
        if contacts:
            emails += [c['email'] for c in self.submission.data.get('contacts',[])]
        perms = {"groups": {}, "users":dict([(email,self.VIEWER_PERMISSIONS) for email in emails]), "email":email}
        return self.set_permissions(perms)
    def update_permissions(self):
        self.permissions = self.get_permissions()
        self.updated = timezone.now()
        self.save()
    def link(self, target, share_path):
        return link_data(self.bioshare_id, target, share_path)
    def get_permissions(self):
        return bioshare_get(GET_PERMISSIONS_URL.format(id=self.bioshare_id))
