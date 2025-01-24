from django import forms
from slims.models import Run, RunLane

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ["run_date", "run_dir", "description", "notes"]

class RunLaneForm(forms.ModelForm):
    class Meta:
        model = RunLane
        fields = ["group", "project_id", "concentration", "description"]

LaneFormSet = forms.inlineformset_factory(Run, RunLane, form=RunLaneForm, extra=1)

class RunWithLanesForm(forms.Form):
    def __init__(self, **kwargs):
        kwargs.pop()
        super().__init__(**kwargs)
    run = RunForm()
    lanes = LaneFormSet(queryset=RunLane.objects.none())  # Pass an empty queryset initially

    def save(self, commit=True):
        # Save the Run instance
        run = self.cleaned_data['run']
        if commit:
            run.save()

        # Save the related Book instances
        lanes = self.cleaned_data['lanes']
        for lane in lanes:
            if lane.cleaned_data:
                lane = lane.save(commit=False)
                lane.run = run
                if commit:
                    lane.save()

        return run