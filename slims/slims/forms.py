from django import forms
from coreomics.models import Submission
from slims.models import Run, RunLane
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div
from .widgets import Select2Widget

class SLIMSRunForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows']=2
        self.fields['notes'].widget.attrs['rows']=2
        # required_fields = ["machine"]
        # for field in required_fields:
        #     self.fields[field].required = True
    class Meta:
        model = Run
        fields = ["run_date", "machine_name", "run_dir", "description", "notes"]
        widgets = {
            'run_date': forms.DateInput(attrs={'type': 'date'})
        }

class RunForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ["machine"]
        self.fields['description'].widget.attrs['rows']=2
        self.fields['notes'].widget.attrs['rows']=2
        for field in required_fields:
            self.fields[field].required = True
    class Meta:
        model = Run
        fields = ["run_date", "machine", "run_dir", "description", "notes"]
        widgets = {
            'run_date': forms.DateInput(attrs={'type': 'date'})
        }

class PacbioRunForm(RunForm):
    pass
    # class Meta:
    #     model = Run
        # fields = ["description", "machine"machine_name", "notes"]

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
    # submission = forms.ModelChoiceField(
    #     queryset=Submission.objects.all(),  # This is not used to pre-populate the select.
    #     required=True,  # The field is required
    #     widget=forms.Select(attrs={'class': 'select2', 'config': 'submission'})
    # )
        # choices=[('', 'Choose submission...')],  # Empty placeholder option
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows']=2
        self.fields['lane_number'].required = True
    # def clean_submission(self):
    #     submission_id = self.cleaned_data['submission']
    #     submission = Submission.objects.filter(id=submission_id).first()
    #     if not submission:
    #         raise forms.ValidationError('Please choose a submission.')
    #     return submission
    class Meta:
        widgets = {
            'lane_number': forms.NumberInput({'class': 'lane-input'}),
            'submission': Select2Widget(attrs={'class': 'select2', 'config': 'submission'})
        }
        labels = {
            'lane_number': 'Lane'
        }
        model = RunLane
        fields = ["lane_number", "submission", "project_id", "lane_dir", "description"]#, "group"

class SLIMSLaneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows']=2
        self.fields['lane_number'].required = True
    class Meta:
        widgets = {
            'lane_number': forms.NumberInput({'class': 'lane-input'}),
            'group': Select2Widget(attrs={'class': 'select2', 'config': 'group'})
        }
        labels = {
            'lane_number': 'Lane'
        }
        model = RunLane
        fields = ["lane_number", "group", "project_id", "lane_dir", "description"]#, "group"

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