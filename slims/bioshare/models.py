from django.db import models
from .config import VIEW_URL, GET_PERMISSIONS_URL, SET_PERMISSIONS_URL, FILESYSTEM_ID, DEFAULT_GROUP, AUTH_TOKEN
from coreomics.models import Submission
from .requests import bioshare_post, bioshare_get, create_share

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
        if not self.bioshare_id:
            name = self.name or '{}: {}'.format(self.submission.pi_name,self.submission.internal_id)
            notes = self.notes or 'Generated from {}'.format(self.submission.internal_id)
            filesystem = FILESYSTEM_ID
            self.bioshare_id = create_share(AUTH_TOKEN, name, notes, filesystem)
        if not self.id:
            self.id = '{}_{}'.format(self.submission.pk, self.bioshare_id)
        instance = super(SubmissionShare, self).save(*args, **kwargs)
        self.share_with_group()
        return instance
        
    @property
    def url(self):
        return VIEW_URL.format(id=self.bioshare_id)
    def set_permissions(self, perms=None):
#         if not perms:
#             perms = {"test": True, "groups": {}, "users":dict([(p.email,["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]) for p in self.submission.participants.all()]), "email":True}
#         print('perms', perms)
#       perms = {"users":{"jdoe@domain.com":["view_share_files","download_share_files","write_to_share","delete_share_files","admin"]},"groups":{"1":["view_share_files","download_share_files","write_to_share"]},"email":true}
        return bioshare_post(SET_PERMISSIONS_URL.format(id=self.bioshare_id), AUTH_TOKEN, perms)
    def share_with_participants(self, email=False):
        perms = {"groups": {}, "users":dict([(p.email, self.ADMIN_PERMISSIONS) for p in self.submission.data['participants']]), "email":email}
        return self.set_permissions(perms)
    def share_with_group(self, email=False):
        if DEFAULT_GROUP:
            perms = {"groups": {DEFAULT_GROUP: self.VIEWER_PERMISSIONS}, "email":email}
            return self.set_permissions(perms)
    def share(self, contacts=False, email=False):
        emails = [self.submission.email, self.submission.pi_email]
        if contacts:
            emails += [c.email for c in self.submission.contacts.all()]
        perms = {"groups": {}, "users":dict([(email,self.VIEWER_PERMISSIONS) for email in emails]), "email":email}
        return self.set_permissions(perms)
    def get_permissions(self):
        return bioshare_get(GET_PERMISSIONS_URL.format(id=self.bioshare_id), AUTH_TOKEN)
