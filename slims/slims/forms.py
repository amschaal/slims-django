from django import forms
from coreomics.models import Submission, Note
from coreomics.utils import format_note
from slims.models import Run, RunLane, LaneData
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
        required_fields = ["machine","run_date"]
        self.fields['type'].disabled = True
        self.fields['description'].widget.attrs['rows']=2
        self.fields['notes'].widget.attrs['rows']=2
        for field in required_fields:
            self.fields[field].required = True
        if self.instance.type:
            self.fields['machine'].queryset = self.instance.type.machines.distinct()

    class Meta:
        model = Run
        fields = ["unique_id", "type", "run_date", "machine", "run_dir", "description", "notes"]
        widgets = {
            'run_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'unique_id': 'Run ID'
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

         # If it's an existing instance, populate metadata fields with values from the model
        if self.instance and self.instance.data:
            data = self.instance.data
            for field_name in list(self.fields.keys()):
                if field_name.startswith('metadata_'):
                    # Extract the key part after 'metadata_'
                    metadata_key = field_name[len('metadata_'):]

                    # Set initial value from the model's meta_data field if the key exists
                    if metadata_key in data:
                        self.fields[field_name].initial = data[metadata_key]
    def clean(self):
        cleaned_data = super().clean()
        data = {}

        # Loop through the fields and collect any 'metadata_*' fields
        for field_name, value in cleaned_data.items():
            if field_name.startswith('metadata_'):
                metadata_key = field_name[len('metadata_'):]  # Get the key part after 'metadata_'
                data[metadata_key] = value

        cleaned_data['data'] = data
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.data = self.cleaned_data.get('data', {})
        if commit:
            instance.save()
        return instance
    # def clean_submission(self):
    #     submission_id = self.cleaned_data['submission']
    #     submission = Submission.objects.filter(id=submission_id).first()
    #     if not submission:
    #         raise forms.ValidationError('Please choose a submission.')
    #     return submission
    class Meta:
        widgets = {
            'lane_number': forms.NumberInput({'class': 'lane-input', 'min': 1}),
            'submission': Select2Widget(attrs={'class': 'select2', 'config': 'submission'})
        }
        labels = {
            'lane_number': 'Unit',
            'lane_dir': 'Pool Directory'
        }
        model = RunLane
        fields = ["lane_number", "submission", "lane_dir", "description"]#, "group"

class SLIMSLaneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows']=2
        self.fields['lane_number'].required = True
    class Meta:
        widgets = {
            'lane_number': forms.NumberInput({'class': 'lane-input', 'min': 1}),
            'group': Select2Widget(attrs={'class': 'select2', 'config': 'group'})
        }
        labels = {
            'lane_number': 'Lane'
        }
        model = RunLane
        fields = ["lane_number", "group", "project_id", "lane_dir", "description"]#, "group"

class NovaSeqLaneForm(RunLaneForm):
    metadata_unaligned = forms.CharField(label="Unaligned Directory", required=False)

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

class LaneDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.lane = kwargs.pop('lane')
        super().__init__(*args, **kwargs)
        # self.fields['lane'].queryset = RunLane.objects.filter(run=self.run)
    def save(self, commit = ...):
        instance = super().save(commit=False)
        if not getattr(instance, 'lane', None):
            instance.lane = self.lane
        if commit:
            instance.save()
        return instance
    class Meta:
        model = LaneData
        fields = ["data_path", "repository_subpath"]

# LaneDataFormSet = forms.modelformset_factory(LaneData, fields=["data_path", "repository_subpath"], extra=1, can_delete=True)

class RunMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea,help_text='Use "{data_urls}" to expand into the list of URLS for the run data for each submission.')
    pools = forms.ModelMultipleChoiceField(queryset=LaneData.objects.all(), widget=forms.CheckboxSelectMultiple)
    test = forms.BooleanField(help_text="Select this to see what messages will be sent to which submissions.", required=False)
    allow_repeat_messages = forms.BooleanField(help_text="Select this to allow repeat messages for a pool.  By default, only one message needs to be sent per pool.", required=False)
    # select_submission = forms.ModelChoiceField(queryset=Submission.objects.none(),help_text="Select a submission to select all pools related to that submission.", required=False)
    # forms.MultipleChoiceField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        self.run = kwargs.pop('run')
        super().__init__(*args, **kwargs)
        self.fields['pools'].queryset = self.run.lanes.all()
        # self.fields['select_submission'].queryset = Submission.objects.filter(lanes__run=self.run).distinct()
    def get_pools(self):
        pools_qs = self.fields['pools'].queryset
        return list(zip(self['pools'], pools_qs))
    def send_message(self):
        message = self.cleaned_data['message']
        pools = self.cleaned_data['pools']
        test = self.cleaned_data['test']
        submissions = Submission.objects.filter(lanes__in=pools).distinct()
        notes = []
        for submission in submissions:
            formatted_note = format_note(message, submission, LaneData.objects.filter(lane__run=self.run, lane__submission=submission, status=LaneData.STATUS_COMPLETE))
            note = Note(submission=submission, template=message, text=formatted_note)
            if not test:
                note.save()
                note.pools.add(*pools.filter(submission=submission))
                # note.send_note()
                # response = submission.create_note(formatted_note)
            notes.append((submission.submission_id, note))
        if not test:
            for submission_id, note in notes:
                try:
                    note.send_note()
                except Exception as e:
                    print(e)
        self.run.update_message_status()
        return notes