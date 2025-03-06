from django import forms
from slims.models import Run, RunLane
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div

class RunForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ["machine"]
        for field in required_fields:
            self.fields[field].required = True
    class Meta:
        model = Run
        fields = ["run_type", "run_date", "machine", "run_dir", "description", "notes"]

class PacbioRunForm(RunForm):
    class Meta:
        model = Run
        fields = ["description", "machine", "notes"]

# Following helper is not working for some reason.
class RunLaneHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.form_horizontal = True
        self.form_tag = False
        self.layout = Layout(
            Div('group', css_class='column is-2'), 
            Div('project_id', css_class='column is-3'),
            Div('description', css_class='column is-5'),
        )

class RunLaneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows']=2
        self.fields['lane_number'].required = True
        # if self.instance:
        #     self.fields['lane_number'].disabled = True
        # self.fields['lane_number'].la = 'foo'
        # self.fields['submission'].queryset = Submission.objects.f
    class Meta:
        widgets = {
            'lane_number': forms.NumberInput({'class': 'lane-input'}),
            'group': forms.Select(attrs={'class': 'select2'})
        }
        labels = {
            'lane_number': 'Lane'
        }
        model = RunLane
        fields = ["lane_number", "group", "submission", "project_id", "lane_dir", "description"]

LaneFormSet = forms.inlineformset_factory(Run, RunLane, form=RunLaneForm, extra=1)

class RunWithLanesForm(forms.Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    run = RunForm()
    lanes = LaneFormSet(queryset=RunLane.objects.none())  # Pass an empty queryset initially

    def save(self, commit=True):
        # Save the Run instance
        run = self.cleaned_data['run']
        if commit:
            run.save()

        # Save the related Lane instances
        lanes = self.cleaned_data['lanes']
        for lane in lanes:
            if lane.cleaned_data:
                lane = lane.save(commit=False)
                lane.run = run
                if commit:
                    lane.save()

        return run