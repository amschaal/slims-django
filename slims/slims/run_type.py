from collections import OrderedDict
from .models import LaneData, RunType, Run, RunLane
from .forms import RunForm, PacbioRunForm, LaneFormSet, RunLaneForm, SLIMSRunForm, SLIMSLaneForm
from django import forms
from django.conf import settings
class  RunTypeBase(object):
    id = 'Run'
    name = 'General Run'
    _run_template = 'run.html'
    _run_form_template = 'run_forms/edit_run.html'
    _run_form = RunForm
    _lane_form = RunLaneForm
    _lane_formset = None#LaneFormSet
    _data_directory_templates = [{'data_path': '{run.machine.base_directory}/{run.run_dir}/Unaligned/Project_{lane.lane_dir}', 'repository_subpath': '{run.run_dir}/{lane.lane_dir}'}]
    # _data_directory_templates = [{'data_path': '/share/example/run/{run.run_dir}/{lane.lane_dir}', 'repository_subpath': 'subfolder/{lane.lane_dir}'}]
    # _data_directory_templates = [{'data_path': '/tmp/{run.run_dir}/{lane.lane_dir}', 'repository_subpath': '{run.run_dir}/{lane.lane_dir}'}]
    def __init__(self, run=None):
        self.run = run
    @property
    def settings(self):
        return settings.RUN_TYPE_OPTIONS.get(self.id, {})
    @property
    def run_template(self):
        return self._run_template
    @property
    def run_form_template(self):
        return self._run_form_template
    @property
    def run_form(self):
        # from .forms import RunForm
        # return RunForm
        return self._run_form
    @property
    def lane_formset(self):
        # from .forms import LaneFormSet
        # return LaneFormSet
        if self._lane_formset:
            return self._lane_formset
        return forms.inlineformset_factory(Run, RunLane, form=self._lane_form, extra=1)
        
    def generate_lane_directories(self, lane):
        directories = []
        for t in self.settings.get('data_directory_templates', self._data_directory_templates):
            data_path = t['data_path'].format(run=self.run, lane=lane)
            if 'repository_subpath' in t:
                repository_subpath = t['repository_subpath'].format(run=self.run, lane=lane)
            else:
                repository_subpath = data_path.split('/')[-1]
            directories.append(LaneData(lane=lane, data_path=data_path, repository_subpath=repository_subpath))
        # instances = [LaneData(lane=lane, data_path=d['data_path'], repository_subpath=d.get('repository_subpath', d['data_path'].split('/')[-1])) for d in directories]
        return directories
    def create_lane_directories(self, lane):
        instances = self.generate_lane_directories(lane)
        lane.directories.exclude(status=LaneData.STATUS_COMPLETE).delete()
        return LaneData.objects.bulk_create(instances)
        # return [t.format(run=self.run, lane=lane) for t in self._data_directory_templates]

class SLIMSRun(RunTypeBase):
    id = 'SLIMSRun'
    name = 'SLIMS Classic'
    _run_template = 'run.html'
    _run_form_template = 'run_forms/edit_run.html'
    _run_form = SLIMSRunForm
    _lane_form = SLIMSLaneForm
    _data_directory_templates = []

class IlluminaRun(RunTypeBase):
    id = 'Illumina'
    name = 'Illumina Run'

class AvitiRun(RunTypeBase):
    id = 'Aviti'
    name = 'Aviti Run'
    _data_directory_templates = [{'data_path': '{run.machine.base_directory}/{run.run_dir}/Unaligned/Project_{lane.lane_dir}', 'repository_subpath': '{run.run_dir}/{lane.lane_dir}'}]

class PacbioRun(RunTypeBase):
    id = 'Pacbio'
    name = 'Pacbio Run'
    # _run_form_template = 'run_forms/pacbio.html'
    _run_form  = PacbioRunForm

class RunTypeRegistry:
    klasses = OrderedDict()
    @classmethod
    def register(cls, klass,):
        if klass.id not in cls.klasses:
            # print('klass.id', klass.id)
            # RunType.objects.get_or_create(id=klass.id, name=klass.name)
            cls.klasses[klass.id] = klass
    @classmethod
    def get(cls, id):
        return cls.klasses.get(id, RunTypeBase)
    @classmethod
    def choices(cls):
        return [(klass.id, klass.name) for id, klass in cls.klasses.items()]
    @classmethod
    def sync_db(cls):
        for id, klass in cls.klasses.items():
            print(RunType.objects.get_or_create(id=klass.id, name=klass.name))
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(RunTypeRegistry, cls).__new__(cls)
    #         return cls.instance
    #     def __init__(self):
    #         self.classes = OrderedDict()
    # def register(self, klass):
    #     if klass.id not in self.classes:
    #         self.classes[klass.id]

# registry = RunTypeRegistry()
run_types = [RunTypeBase, IlluminaRun, PacbioRun, SLIMSRun, AvitiRun]
for r in run_types:
    RunTypeRegistry.register(r)