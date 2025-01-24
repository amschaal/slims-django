from django.forms import ModelForm
from slims.models import Run, RunLane

class RunForm(ModelForm):
    class Meta:
        model = Run
        fields = ["run_date", "run_dir", "description", "notes"]