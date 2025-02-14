from django.db import models
from django.utils import timezone

class Submission(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    internal_id = models.CharField(max_length=25, null=True)
    submitted = models.DateTimeField(null=True)
    last_sync = models.DateTimeField(null=True)
    data = models.JSONField(default=dict)
    def update(self, serialized, commit=True):
        self.data = serialized
        self.internal_id = serialized['internal_id']
        self.last_sync = timezone.now()
        if commit:
            self.save()
    @staticmethod
    def import_submission(serialized):
        submission = Submission(id=serialized['id'], submitted=serialized['submitted'])
        submission.update(serialized, commit=True)
        return submission