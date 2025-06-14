from django.db import models
from django.utils import timezone

# from slims.models import RunLane, LaneData

class Submission(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    internal_id = models.CharField(max_length=25, null=True)
    submission_type = models.CharField(max_length=100, null=True)
    submitted = models.DateTimeField(null=True)
    submitter_name = models.CharField(max_length=75, null=True)
    submitter_email = models.EmailField(max_length=75, null=True)
    pi_name = models.CharField(max_length=75, null=True)
    pi_email = models.EmailField(max_length=75, null=True)
    url = models.URLField(null=True)
    last_sync = models.DateTimeField(null=True)
    data = models.JSONField(default=dict)
    class Meta:
        ordering = ('-submitted',)
    def __str__(self):
        return str(self.submitted)[:10] + ': ' + (self.internal_id or self.id)
    @property
    def submission_id(self):
        return self.internal_id or self.id
    def update(self, data=None, commit=True):
        if data:
            # print(data['updated'], self.data)
            # if self.data and self.data['updated'] and (self.data['updated'] >= data['updated']):
            #     print('###No need to update {}###'.format(self.id))
            #     return
            self.data = data
        # print('***Updating {} ***'.format(self.id))
        self.internal_id = self.data['internal_id']
        self.submission_type = self.data['type']['name']
        self.submitter_name = self.data['last_name'] + ', ' + self.data['first_name']
        self.submitter_email = self.data['email']
        self.pi_name = self.data['pi_last_name'] + ', ' + self.data['pi_first_name']
        self.pi_email = self.data['pi_email']
        self.url = self.data['url']
        self.last_sync = timezone.now()
        if commit:
            self.save()
    @staticmethod
    def import_submission(serialized):
        submission = Submission(id=serialized['id'], submitted=serialized['submitted'])
        submission.update(serialized, commit=True)
        return submission
    def create_share(self, email=False):
        from bioshare.models import SubmissionShare
        if hasattr(self, 'share'):
            return self.share
        share = SubmissionShare(submission=self)
        share.save()
        # share.update_permissions()
        share.share_with_group_and_participants(email=email)
        return share
    def link_share(self):
        from .utils import link_share
        if hasattr(self, 'share'):
            link_share(self, self.share)
    # def create_note(self, note):
    #     from .utils import create_note
    #     return create_note(self, note)

class Note(models.Model):
    coreomics_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    template = models.TextField(null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True)
    data = models.JSONField(null=True)
    pools = models.ManyToManyField('slims.RunLane', symmetrical=True, related_name="notes")
    def __str__(self):
        return '{submission}: {created}'.format(submission=self.submission.submission_id, created=self.created)
    def send_note(self, asynchronous=False):
        # print('****Creating Note****')
        from .utils import send_note
        from threading import Thread
        if asynchronous:
            # print ("create note asynchronously!!!!!!!!!!")
            Thread(target=send_note, args=(self.id,)).start()
        else:
            send_note(self)
    @property
    def sent_to(self):
        if self.coreomics_id and self.data:
            return list(set(self.data['emails']))