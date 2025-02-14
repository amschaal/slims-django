from .forms import RunForm, LaneFormSet


class  RunType(object):
    _run_template = 'run.html'
    _run_form = RunForm
    _lane_formset = LaneFormSet
    def __init__(self, run=None):
        self.run = run
    @property
    def run_template(self):
        return self._run_template
    @property
    def run_form(self):
        return self._run_form
    @property
    def lane_formset(self):
        return self._lane_formset
    