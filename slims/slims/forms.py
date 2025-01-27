from django import forms
from slims.models import Run, RunLane
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ["run_date", "run_dir", "description", "notes"]

class RunLaneHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_horizontal = True
        self.layout = Layout(
            Div(
                Div('group', css_class='column is-2'), 
                Div('project_id', css_class='column is-3'),
                Div('concentration', css_class='column is-1'),
                Div('description', css_class='column is-6'),
                css_class='columns is-multiline'
            )
        )

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

        # Save the related Lane instances
        lanes = self.cleaned_data['lanes']
        for lane in lanes:
            if lane.cleaned_data:
                lane = lane.save(commit=False)
                lane.run = run
                if commit:
                    lane.save()

        return run